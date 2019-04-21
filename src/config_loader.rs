//! Provider for deployment configuration

use dotenv::dotenv;
use std::env::var;
use std::error::Error;
use std::fmt::Debug;

/// Provider for deployment configuration
pub trait ConfigLoader: Debug {
    /// Returns the address that the elasticsearch instance is running on
    fn elasticsearch_address(&self) -> Result<String, Box<dyn Error>>;

    /// Returns the port that the elasticsearch instance is running on
    fn elasticsearch_port(&self) -> Result<u16, Box<dyn Error>>;

    /// Returns the address that the server will run on
    fn server_address(&self) -> Result<String, Box<dyn Error>>;

    /// Returns the port that the server will run on
    fn server_port(&self) -> Result<u16, Box<dyn Error>>;

    /// Returns the path to a file that contains the definition of all items
    fn items_file(&self) -> Result<String, Box<dyn Error>>;
}

/// Provides configurations found in environment variables, loading them
/// out of a .env file first if available
#[derive(Debug)]
#[non_exhaustive]
pub struct DotEnvConfigLoader;

impl DotEnvConfigLoader {
    /// Creates a new instance of [`DotEnvConfigLoader`] and loads env vars
    /// defined in a .env file if available
    pub fn new() -> Self {
        let loading_result = dotenv();
        if loading_result.is_err() {
            println!("No .env file was found, using only pre-defined env vars.")
        };
        Self {}
    }
}

impl Default for DotEnvConfigLoader {
    fn default() -> Self {
        Self::new()
    }
}

impl ConfigLoader for DotEnvConfigLoader {
    fn elasticsearch_address(&self) -> Result<String, Box<dyn Error>> {
        Ok(var("ELASTICSEARCH_ADDRESS")?)
    }

    fn elasticsearch_port(&self) -> Result<u16, Box<dyn Error>> {
        Ok(var("ELASTICSEARCH_PORT")?.parse()?)
    }

    fn server_address(&self) -> Result<String, Box<dyn Error>> {
        Ok(var("SERVER_ADDRESS")?)
    }

    fn server_port(&self) -> Result<u16, Box<dyn Error>> {
        Ok(var("SERVER_PORT")?.parse()?)
    }

    fn items_file(&self) -> Result<String, Box<dyn Error>> {
        Ok(var("ITEMS_FILE")?)
    }
}
