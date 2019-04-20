//! Constants that should be extracted to env vars

/// The address that the elasticsearch instance is running on
pub const ELASTICSEARCH_ADDRESS: &str = "http://localhost";

/// The port that the elasticsearch instance is running on
pub const ELASTICSEARCH_PORT: u16 = 9200;

/// The address that the server should run on
pub const SERVER_ADDRESS: &str = "localhost";
/// The port that the server should run on
pub const PORT: u16 = 8080;

/// A TOML file containing definitions for all items
pub const ITEMS_TOML: &str = "items.toml";
