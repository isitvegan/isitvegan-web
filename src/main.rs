use is_it_vegan::search_engine::{ElasticSearch, SearchEngine};

fn main() {
    let search_engine = ElasticSearch::try_new(ELASTICSEARCH_SERVER_URL).unwrap();
    for item in search_engine.search("Milk").unwrap() {
        println!("{:#?}", item);
    }
}

const ELASTICSEARCH_SERVER_URL: &str = "http://localhost:9200";
