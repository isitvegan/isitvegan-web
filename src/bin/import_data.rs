use is_it_vegan::{
    model::Item,
    model::State,
    search_engine::{ElasticSearch, SearchEngine},
    constant::*
};

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

    search_engine.wipe_storage().unwrap();
    search_engine.import_items(&[item]).unwrap();
}
