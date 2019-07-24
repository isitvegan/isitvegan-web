//! Data sources for items

use crate::model::{Source, State};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::error::Error;
use std::fs::File;
use std::io::Read;
use std::path::MAIN_SEPARATOR;
use walkdir::{DirEntry, WalkDir};

/// All available items
#[derive(Debug, Serialize, Deserialize)]
pub struct Items {
    /// The items
    pub items: Vec<Item>,
}

/// The description of an item.
#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    /// The item's name or title.
    pub name: String,

    /// Alternative valid names for this item.
    pub alternative_names: Vec<String>,

    /// [E number] assigned to this item.
    ///
    /// [E number](https://en.wikipedia.org/wiki/E_number)
    pub e_number: Option<String>,

    /// The item's vegan-ness.
    pub state: State,

    /// A text describing what the item and how it's typically used.
    pub description: String,

    /// List of sources for the item's state.
    #[serde(default)]
    pub sources: Vec<Source>,

    /// Common vegan alternatives to this item.
    pub vegan_alternatives: Vec<String>,
}

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
        let imported_items_directory =
            format!("{}{}{}", self.items_directory, MAIN_SEPARATOR, "imported");

        println!("Loading imported items");
        let imported_entries = WalkDir::new(&imported_items_directory)
            .follow_links(true)
            .into_iter()
            .filter_map(|entry| match entry {
                Ok(entry) => Some(entry),
                Err(error) => {
                    println!("Failed to load a filesystem item: {}", error);
                    None
                }
            });
        let imported_items = load_items_from_entries(imported_entries)?;
        println!("Finished loading imported items");

        println!("Loading manual items");
        let manual_entries = WalkDir::new(&self.items_directory)
            .follow_links(true)
            .into_iter()
            .filter_map(|entry| match entry {
                Ok(entry) => Some(entry),
                Err(error) => {
                    println!("Failed to load a filesystem item: {}", error);
                    None
                }
            })
            .filter(|entry| {
                !entry
                    .path()
                    .to_string_lossy()
                    .contains(&imported_items_directory)
            });
        let manual_items = load_items_from_entries(manual_entries)?;
        println!("Finished loading manual items");

        println!("Resolving duplicated items");
        let unique_items: HashMap<_, _> = imported_items
            .into_iter()
            .chain(manual_items.into_iter())
            .collect();
        let items: Vec<_> = unique_items.into_iter().map(|(_, item)| item).collect();
        println!("Finished importing items");

        Ok(Items { items })
    }
}

fn load_items_from_entries(entries: impl Iterator<Item = DirEntry>) -> Result<HashMap<String, Item>, Box<dyn Error>> {
    let items = entries
        .map(|entry| entry.path().to_string_lossy().into_owned())
        .filter(|file_path| file_path.ends_with(".toml"))
        .map(|file_path| load_items_from_file(&file_path))
        .collect::<Result<Vec<_>, _>>()?
        .into_iter()
        .map(|items| items.items.into_iter())
        .flatten()
        .map(|item| (item.name.clone(), item))
        .collect();
    Ok(items)
}

fn load_items_from_file(file_path: &str) -> Result<Items, Box<dyn Error>> {
    println!("Loading items from {}", file_path);
    let mut file = File::open(file_path)?;
    let mut file_content = String::new();
    file.read_to_string(&mut file_content)?;

    Ok(toml::from_str(&file_content)?)
}
