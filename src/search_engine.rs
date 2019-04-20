//! Client for the communication with the underlying search engine

use crate::model::Item;
use elastic::prelude::*;
use serde_json::json;
use std::error::Error;
use std::fmt::{self, Debug};

/// A search engine for our items
pub trait SearchEngine: Debug + Sync + Send {
    /// Add an item to the search engine
    fn add_item(&self, items: &Item) -> Result<(), Box<dyn Error>>;

    /// Remove all items from the internal storage
    fn wipe_storage(&self) -> Result<(), Box<dyn Error>>;

    /// Search for a query
    fn search(&self, query: &str) -> Result<Vec<Item>, Box<dyn Error>>;
}

/// Search engine with an ElasticSearch backend
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
    fn add_item(&self, item: &Item) -> Result<(), Box<dyn Error>> {
        unimplemented!()
    }

    fn search(&self, query: &str) -> Result<Vec<Item>, Box<dyn Error>> {
        Ok(self
            .client
            .search::<Item>()
            .index(INDEX)
            .body(json!({
                "query": {
                    "query_string": {
                        "query": query
                    }
                }
            }))
            .send()
            .map_err(Box::new)?
            .into_hits()
            .filter_map(|hit| hit.into_document())
            .collect())
    }
}

const INDEX: &str = "items";
