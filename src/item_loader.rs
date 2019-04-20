//! Data sources for items

use crate::model::Items;
use std::error::Error;
use std::fs::File;
use std::io::Read;

/// A data source for items
pub trait ItemLoader {
    /// Load items from an underlying source
    fn load_items(&self) -> Result<Items, Box<dyn Error>>;
}


/// An implementation of [`ItemLoader`] that uses a toml file from the file system
#[derive(Debug)]
pub struct TomlItemLoader {
    file_path: String
}

impl TomlItemLoader {
    /// Create a new [`TomlItemLoader`] that will load items from a specified file
    pub fn new(file_path: String) -> TomlItemLoader {
        Self {
            file_path
        }
    }
}

impl ItemLoader for TomlItemLoader {
    fn load_items(&self) -> Result<Items, Box<dyn Error>> {
        let mut file = File::open(&self.file_path)?;
        let mut file_content = String::new();
        file.read_to_string(&mut file_content)?;


        Ok(toml::from_str(&file_content)?)
    }
}
