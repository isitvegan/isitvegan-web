//! Client for the communication with the underlying search engine

use crate::data::Item;
use elastic::prelude::*;
use serde_json::json;
use std::fmt::{self, Debug};

/// A search engine for our items
pub trait SearchEngine {
    /// Search for a query
    fn search(self, query: &str) -> Result<Vec<Item>, elastic::Error>;
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
    pub fn try_new() -> Result<ElasticSearch, elastic::Error> {
        Ok(Self {
            client: SyncClientBuilder::new().build()?,
        })
    }
}

impl SearchEngine for ElasticSearch {
    fn search(self, query: &str) -> Result<Vec<Item>, elastic::Error> {
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
            .send()?
            .into_hits()
            .map(|hit| hit.into_document().unwrap())
            .collect())
    }
}
