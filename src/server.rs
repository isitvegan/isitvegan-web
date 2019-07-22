//! The server running the application

use crate::model::Item;
use crate::search_engine::SearchEngine;
use rocket::config::{Config, Environment};
use rocket::http::RawStr;
use rocket::request::FromFormValue;
use rocket::State;
use rocket_contrib::json::Json;
use std::error::Error;
use std::fmt::Debug;
use std::sync::Arc;

/// The server running the application
pub trait Server: Debug {
    /// Start the application on the specified port
    fn run(self: Box<Self>, address: &str, port: u16) -> Result<(), Box<dyn Error>>;
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

impl Server for RocketServer {
    fn run(self: Box<Self>, address: &str, port: u16) -> Result<(), Box<dyn Error>> {
        let config = Config::build(Environment::Staging)
            .address(address)
            .port(port)
            .finalize()
            .map_err(Box::new)?;

        rocket::custom(config)
            .mount("/", routes![search, item_by_slug])
            .manage(self.search_engine)
            .launch();

        Ok(())
    }
}

/// The selected search scope
#[derive(Debug)]
pub enum Scope {
    /// Search by name and alternative names
    Names,
    /// Search only e numbers
    ENumber,
}

impl<'v> FromFormValue<'v> for Scope {
    type Error = &'v RawStr;

    fn from_form_value(form_value: &'v RawStr) -> Result<Self, &'v RawStr> {
        let decoded_value = form_value.percent_decode().map_err(|_| form_value)?;
        match decoded_value.as_ref() {
            "names" => Ok(Scope::Names),
            "eNumber" => Ok(Scope::ENumber),
            _ => Err(form_value),
        }
    }
}

/// Searches a single item with a scope
#[get("/search?<query>&<scope>")]
fn search(
    query: String,
    scope: Scope,
    search_engine: State<'_, Arc<dyn SearchEngine>>,
) -> Result<Json<Vec<Item>>, Box<dyn Error>> {
    let results = match scope {
        Scope::Names => search_engine.search_by_names(&query),
        Scope::ENumber => search_engine.search_by_e_number(&query),
    };
    results.map(Json)
}

/// Searches a single item per slug
#[get("/items/<slug>")]
fn item_by_slug(
    slug: String,
    search_engine: State<'_, Arc<dyn SearchEngine>>,
) -> Result<Option<Json<Item>>, Box<dyn Error>> {
    search_engine
        .get_by_slug(&slug)
        .map(|option| option.map(Json))
}
