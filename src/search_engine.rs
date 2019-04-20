//! Client for the communication with the underlying search engine

use crate::model::Item;
use elastic::prelude::*;
use serde_json::json;
use std::error::Error;
use std::fmt::{self, Debug};

/// A search engine for our items
pub trait SearchEngine: Debug {
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
    /// Create a new [`ElasticSearch`] instant
    pub fn try_new(server_url: &str) -> Result<ElasticSearch, elastic::Error> {
        Ok(Self {
            client: SyncClientBuilder::new().static_node(server_url).build()?,
        })
    }
}

impl SearchEngine for ElasticSearch {
    fn search(&self, query: &str) -> Result<Vec<Item>, Box<dyn Error>> {
        Ok(self
            .client
            .search::<Item>()
            .index("_all")
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
