use is_it_vegan::search_engine::{ElasticSearch, SearchEngine};
use is_it_vegan::server::{RocketServer, Server};
use std::sync::Arc;

fn main() {
    let search_engine = ElasticSearch::try_new(ELASTICSEARCH_ADDRESS, ELASTICSEARCH_PORT).unwrap();
    for item in search_engine.search("Milk").unwrap() {
        println!("{:#?}", item);
    }

    let server = Box::new(RocketServer::new(Arc::new(search_engine)));
    server.run(SERVER_ADDRESS, PORT).unwrap();
}

const ELASTICSEARCH_ADDRESS: &str = "http://localhost";
const ELASTICSEARCH_PORT: u16 = 9200;

const SERVER_ADDRESS: &str = "localhost";
const PORT: u16 = 8080;
