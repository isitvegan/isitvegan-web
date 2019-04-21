//! Data sources for items

use crate::model::Items;
use std::error::Error;
use std::fs::File;
use std::io::Read;
use walkdir::WalkDir;

/// A data source for items
pub trait ItemLoader {
    /// Load items from an underlying source
    fn load_items(&self) -> Result<Items, Box<dyn Error>>;
}

/// An implementation of [`ItemLoader`] that uses a toml file from the file system
#[derive(Debug)]
pub struct TomlItemLoader {
    items_directory: String,
}

impl TomlItemLoader {
    /// Create a new [`TomlItemLoader`] that will load items from toml files in a specified directory
    pub fn new(items_directory: String) -> TomlItemLoader {
        Self { items_directory }
    }
}

impl ItemLoader for TomlItemLoader {
    fn load_items(&self) -> Result<Items, Box<dyn Error>> {
        let items: Vec<_> = WalkDir::new(&self.items_directory)
            .follow_links(true)
            .into_iter()
            .filter_map(Result::ok)
            .map(|entry| entry.into_path().to_string_lossy().into_owned())
            .filter(|file_path| file_path.ends_with(".toml"))
            .map(|file_path| load_items_from_file(&file_path).into_iter())
            .flatten()
            .map(|items| items.items.into_iter())
            .flatten()
            .collect();
        Ok(Items { items })
    }
}

fn load_items_from_file(file_path: &str) -> Result<Items, Box<dyn Error>> {
    let mut file = File::open(file_path)?;
    let mut file_content = String::new();
    file.read_to_string(&mut file_content)?;

    Ok(toml::from_str(&file_content)?)
}
