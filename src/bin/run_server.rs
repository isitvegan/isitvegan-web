use is_it_vegan::{
    search_engine::ElasticSearch,
    server::{RocketServer, Server},
    constant::*
};
use std::sync::Arc;

fn main() {
    let search_engine = ElasticSearch::try_new(ELASTICSEARCH_ADDRESS, ELASTICSEARCH_PORT).unwrap();

    let server = Box::new(RocketServer::new(Arc::new(search_engine)));
    server.run(SERVER_ADDRESS, PORT).unwrap();
}

