use is_it_vegan::{
    config_loader::{ConfigLoader, DotEnvConfigLoader},
    search_engine::ElasticSearch,
    server::{RocketServer, Server},
};
use std::sync::Arc;

#[rocket::main]
async fn main() {
    let config_loader = DotEnvConfigLoader::new();
    let server_address = config_loader.server_address().unwrap();
    let server_port = config_loader.server_port().unwrap();

    let search_engine = ElasticSearch::try_new(
        &config_loader.elasticsearch_address().unwrap(),
        config_loader.elasticsearch_port().unwrap(),
    )
    .unwrap();

    let server = Box::new(RocketServer::new(Arc::new(search_engine)));
    server
        .run(
            server_address,
            server_port,
        )
        .await
        .unwrap();
}
