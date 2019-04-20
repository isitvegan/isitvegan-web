use is_it_vegan::search_engine::{ElasticSearch, SearchEngine};
use is_it_vegan::server::{RocketServer, Server};

fn main() {
    let search_engine = ElasticSearch::try_new(ELASTICSEARCH_SERVER_URL).unwrap();
    for item in search_engine.search("Milk").unwrap() {
        println!("{:#?}", item);
    }

    let server = RocketServer::new(Box::new(search_engine));
    server.run(SERVER_URL, PORT).unwrap();
}

const ELASTICSEARCH_SERVER_URL: &str = "http://localhost:9200";
const SERVER_URL: &str = "localhost";
const PORT: u16 = 8080;
