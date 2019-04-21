use is_it_vegan::{
    config_loader::{ConfigLoader, DotEnvConfigLoader},
    item_loader::{ItemLoader, TomlItemLoader},
    search_engine::{ElasticSearch, SearchEngine},
};

fn main() {
    let config_loader = DotEnvConfigLoader::new();

    let search_engine = ElasticSearch::try_new(
        &config_loader.elasticsearch_address().unwrap(),
        config_loader.elasticsearch_port().unwrap(),
    )
    .unwrap();
    let item_loader = TomlItemLoader::new(config_loader.items_file().unwrap());

    let items = item_loader.load_items().unwrap();

    search_engine.wipe_storage().unwrap();
    search_engine.import_items(&items.items).unwrap();
}
