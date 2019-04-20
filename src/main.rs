use is_it_vegan::search_engine::{ElasticSearch, SearchEngine};

fn main() {
    let search_engine = ElasticSearch::try_new().unwrap();
    for item in search_engine.search("Milk").unwrap() {
        println!("{:#?}", item);
    }
}
