//! Client for the communication with the underlying search engine

use crate::model::Item;
use elastic::client::responses::search::Hit;
use elastic::prelude::*;
use serde_json::json;
use std::error::Error;
use std::fmt::{self, Debug};

/// A search engine for our items
pub trait SearchEngine: Debug + Sync + Send {
    /// Import a bunch of items into the search engine's storage
    fn import_items(&self, items: &[Item]) -> Result<(), Box<dyn Error>>;

    /// Remove all items from the internal storage
    fn wipe_storage(&self) -> Result<(), Box<dyn Error>>;

    /// Search for a query
    fn search(&self, query: &str) -> Result<Vec<Item>, Box<dyn Error>>;

    /// Searches for an item by its slug
    fn get_by_slug(&self, slug: &str) -> Result<Option<Item>, Box<dyn Error>>;
}

/// Search engine with an `ElasticSearch` backend
pub struct ElasticSearch {
    client: SyncClient,
}

impl Debug for ElasticSearch {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "client")
    }
}

impl ElasticSearch {
    /// Create a new [`ElasticSearch`] instance
    pub fn try_new(address: &str, port: u16) -> Result<ElasticSearch, elastic::Error> {
        let url = format!("{}:{}", address, port);
        Ok(Self {
            client: SyncClientBuilder::new().static_node(url).build()?,
        })
    }
}

impl SearchEngine for ElasticSearch {
    fn import_items(&self, items: &[Item]) -> Result<(), Box<dyn Error>> {
        if items.is_empty() {
            return Ok(());
        }

        let operations = items.iter().enumerate().map(|(index, item)| {
            bulk_raw()
                .index(serde_json::to_value(item).unwrap())
                .ty(TYPE)
                .id(index)
        });
        self.client
            .bulk()
            .index(INDEX)
            .ty(TYPE)
            .extend(operations)
            .send()?;
        Ok(())
    }

    fn wipe_storage(&self) -> Result<(), Box<dyn Error>> {
        if self.client.index(INDEX).exists().send()?.exists() {
            self.client.index(INDEX).delete().send()?;
        }

        self.client
            .index(INDEX)
            .create()
            .body(json!({
                "settings": {
                    "analysis": {
                        "analyzer": {
                            "autocomplete": {
                                "tokenizer": "autocomplete",
                                "filter": [
                                    "lowercase"
                                ]
                            },
                            "autocomplete_search": {
                                "tokenizer": "lowercase"
                            }
                        },
                        "tokenizer": {
                            "autocomplete": {
                                "type": "edge_ngram",
                                "min_gram": 2,
                                "max_gram": 20,
                                "token_chars": [
                                    "letter",
                                    "digit"
                                ]
                            }
                        }
                    }
                },
                "mappings": {
                    "item": {
                        "properties": {
                            "name": {
                                "type": "text",
                                "analyzer": "autocomplete",
                                "search_analyzer": "autocomplete_search"
                            },
                            "alternative_names": {
                                "type": "text",
                                "analyzer": "autocomplete",
                                "search_analyzer": "autocomplete_search"
                            },
                            "e_number": {
                                "type": "text",
                                "analyzer": "autocomplete"
                            },
                            "description": {
                                "type": "text",
                                "analyzer": "autocomplete",
                                "search_analyzer": "autocomplete_search"
                            },
                            "slug": {
                                "type": "keyword"
                            }
                        }
                    }
                }
            }))
            .send()?;

        Ok(())
    }

    fn search(&self, query: &str) -> Result<Vec<Item>, Box<dyn Error>> {
        Ok(self
            .client
            .search::<Item>()
            .index(INDEX)
            .body(json!({
                "query": {
                    "bool": {
                        "should": [
                            {
                                "term": {
                                    "e_number": {
                                        "value": query,
                                        "boost": 100
                                    }
                                }
                            }, {
                                "multi_match": {
                                    "query": query,
                                    "fields": ["name^4", "e_number^4", "alternative_names^3"],
                                }
                            }
                        ]
                    }
                }
            }))
            .send()
            .map_err(Box::new)?
            .into_hits()
            .filter_map(Hit::into_document)
            .collect())
    }

    fn get_by_slug(&self, slug: &str) -> Result<Option<Item>, Box<dyn Error>> {
        Ok(self
            .client
            .search::<Item>()
            .index(INDEX)
            .body(json!({
                "query": {
                    "term": {
                        "slug": slug
                    }
                }
            }))
            .send()
            .map_err(Box::new)?
            .into_hits()
            .filter_map(Hit::into_document)
            .next())
    }
}

const INDEX: &str = "items";
const TYPE: &str = "item";
