//! Types dealing with the packaging of all items at once.

use crate::model::Item;
use std::error::Error;
use std::fs;
use std::path::Path;

/// Packs all items into a file.
pub trait ItemPacker {
    /// Packs all items into a file at the target path.
    fn pack(&self, items: &[Item], target_file_path: &Path) -> Result<(), Box<dyn Error>>;
}

/// Implementation of [`ItemPacker`\ that stores all items as JSON.
#[derive(Debug, Default)]
pub struct JsonItemPacker;

impl JsonItemPacker {
    /// Construct a new [`JsonItemsPacker`]
    pub fn new() -> Self {
        Self {}
    }
}

impl ItemPacker for JsonItemPacker {
    fn pack(&self, items: &[Item], target_file_path: &Path) -> Result<(), Box<dyn Error>> {
        let json = serde_json::to_string(items)?;
        fs::write(target_file_path, json)?;
        Ok(())
    }
}
