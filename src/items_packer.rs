//! Types dealing with the packaging of all items at once.

use crate::model::Items;
use std::error::Error;
use std::fs;
use std::path::Path;

/// Packs all items into a file.
pub trait ItemsPacker {
    /// Packs all items into a file at the target path.
    fn pack(&self, items: &Items, target_file_path: &Path) -> Result<(), Box<dyn Error>>;
}

/// Implementation of [`AllItemsPacker`\ that stores all items as JSON.
#[derive(Debug)]
pub struct JsonItemsPacker;

impl JsonItemsPacker {
    fn pack(&self, items: &Items, target_file_path: &Path) -> Result<(), Box<dyn Error>> {
        let json = serde_json::to_string(items)?;
        fs::write(target_file_path, json)?;
        Ok(())
    }
}
