//! The server running the application

use crate::model::Item;
use crate::search_engine::SearchEngine;
use async_trait::async_trait;
use rocket::config::Config;
use rocket::form::FromFormField;
use rocket::http::Status;
use rocket::serde::json::Json;
use rocket::State;
use std::error::Error;
use std::fmt::Debug;
use std::net::IpAddr;
use std::sync::Arc;

/// The server running the application
#[async_trait]
pub trait Server: Debug {
    /// Start the application on the specified port
    async fn run(self: Box<Self>, address: IpAddr, port: u16) -> Result<(), Box<dyn Error>>;
}

/// An implementation of [`Server`] that uses [Rocket]
///
/// [Rocket]: https://www.rocket.rs
#[derive(Debug)]
pub struct RocketServer {
    search_engine: Arc<dyn SearchEngine>,
}

impl RocketServer {
    /// Creates a new [`RocketServer`]
    pub fn new(search_engine: Arc<dyn SearchEngine>) -> RocketServer {
        Self { search_engine }
    }
}

#[async_trait]
impl Server for RocketServer {
    async fn run(self: Box<Self>, address: IpAddr, port: u16) -> Result<(), Box<dyn Error>> {
        let config = Config {
            address,
            port,
            ..Default::default()
        };

        _ = rocket::custom(config)
            .mount("/", routes![search, item_by_slug])
            .manage(self.search_engine)
            .launch()
            .await?;

        Ok(())
    }
}

/// The selected search scope
#[derive(Debug, FromFormField)]
pub enum Scope {
    /// Search by name and alternative names
    #[field(value = "names")]
    Names,
    /// Search only e numbers
    #[field(value = "eNumber")]
    ENumber,
}

/// Searches a single item with a scope
#[get("/search?<query>&<scope>")]
fn search(
    query: String,
    scope: Scope,
    search_engine: &State<Arc<dyn SearchEngine>>,
) -> Result<Json<Vec<Item>>, Status> {
    let results = match scope {
        Scope::Names => search_engine.search_by_names(&query),
        Scope::ENumber => search_engine.search_by_e_number(&query),
    };
    results.map(Json).map_err(|_| Status::InternalServerError)
}

/// Searches a single item per slug
#[get("/items/<slug>")]
fn item_by_slug(
    slug: String,
    search_engine: &State<Arc<dyn SearchEngine>>,
) -> Result<Option<Json<Item>>, Status> {
    search_engine
        .get_by_slug(&slug)
        .map(|option| option.map(Json))
        .map_err(|_| Status::InternalServerError)
}
