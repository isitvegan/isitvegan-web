use is_it_vegan::model::Item;
use is_it_vegan::model::State;
use is_it_vegan::search_engine::{ElasticSearch, SearchEngine};
use is_it_vegan::server::{RocketServer, Server};
use std::sync::Arc;

fn main() {
    let search_engine = ElasticSearch::try_new(ELASTICSEARCH_ADDRESS, ELASTICSEARCH_PORT).unwrap();

    let item = Item {
        name: "Butter".to_string(),
        alternative_names: vec!["Titty juice".to_string()],
        e_numbers: vec![],
        state: State::Carnist,
        description: "Not your mom, not your milk!".to_string(),
        sources: vec![],
        vegan_alternatives: vec!["Soy Milk".to_string(), "Oat Milk".to_string()],
    };

    search_engine.wipe_storage();
    search_engine.import_items(&[item]).unwrap();

    let server = Box::new(RocketServer::new(Arc::new(search_engine)));
    server.run(SERVER_ADDRESS, PORT).unwrap();
}

const ELASTICSEARCH_ADDRESS: &str = "http://localhost";
const ELASTICSEARCH_PORT: u16 = 9200;

const SERVER_ADDRESS: &str = "localhost";
const PORT: u16 = 8080;
