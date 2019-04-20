use is_it_vegan::{
    constant::*,
    model::Item,
    model::Source,
    model::State,
    search_engine::{ElasticSearch, SearchEngine},
};
use url::Url;

fn main() {
    let search_engine = ElasticSearch::try_new(ELASTICSEARCH_ADDRESS, ELASTICSEARCH_PORT).unwrap();

    let items = test_data();

    search_engine.wipe_storage().unwrap();
    search_engine.import_items(&items).unwrap();
}

fn test_data() -> Vec<Item> {
    vec![
        Item {
            name: "Butter".to_string(),
            alternative_names: vec!["Titty juice".to_string()],
            e_numbers: vec![],
            state: State::Carnist,
            description: "Not your mom, not your milk!".to_string(),
            sources: vec![],
            vegan_alternatives: vec!["Soy Milk".to_string(), "Oat Milk".to_string()],
        },
        Item {
            name: "Oat Milk".to_string(),
            alternative_names: vec!["Sexy Juice".to_string()],
            e_numbers: vec![],
            state: State::Vegan,
            description: "It's like milk, but for humans.".to_string(),
            sources: vec![Source::Url(Url::parse("https://www.oatly.com").unwrap())],
            vegan_alternatives: vec![],
        },
    ]
}
