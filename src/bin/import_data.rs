use is_it_vegan::{
    config_loader::{ConfigLoader, DotEnvConfigLoader},
    item_loader::{ItemLoader, TomlItemLoader},
    item_mapper::{ItemMapper, ItemMapperImpl},
    search_engine::{ElasticSearch, SearchEngine},
};

fn main() {
    let config_loader = DotEnvConfigLoader::new();

    let search_engine = ElasticSearch::try_new(
        &config_loader.elasticsearch_address().unwrap(),
        config_loader.elasticsearch_port().unwrap(),
    )
    .unwrap();

    let item_loader = TomlItemLoader::new(config_loader.items_directory().unwrap());
    let item_mapper = ItemMapperImpl::new();

    let source_items = item_loader.load_items().unwrap();
    let items = item_mapper.map_items(source_items);

    if items.is_empty() {
        eprintln!("No items could be imported. Is the path to the items directory correct?");
    }

    search_engine.wipe_storage().unwrap();
    search_engine.import_items(&items).unwrap();
}
