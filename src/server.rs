//! The server running the application

use crate::search_engine::SearchEngine;
use rocket::config::{Config, Environment};
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
            .mount("/", routes![index])
            .manage(self.search_engine)
            .launch();

        Ok(())
    }
}

/// Returns a hello world
#[get("/search/<query>")]
fn index(query: String) -> &'static str {
    "Hello, world!"
}
