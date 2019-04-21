//! Maps items to their model representation

use crate::item_loader;
use crate::model;
use slug::slugify;
use std::fmt::Debug;

/// Maps items from their source representation
/// to the desired representation for elastic.
pub trait ItemMapper: Debug {
    /// Maps the items to the desired representation for elastic.
    fn map_items(&self, items: item_loader::Items) -> Vec<model::Item>;
}

/// Default implementation of [`ItemMapper`].
#[derive(Debug)]
pub struct ItemMapperImpl;

impl ItemMapperImpl {
    /// Creates a new [`ItemMapperImpl`].
    pub fn new() -> Self {
        ItemMapperImpl
    }
}

impl ItemMapper for ItemMapperImpl {
    fn map_items(&self, items: item_loader::Items) -> Vec<model::Item> {
        items.items.into_iter().map(map_item).collect()
    }
}

fn map_item(
    item_loader::Item {
        name,
        alternative_names,
        e_number,
        state,
        description,
        sources,
        vegan_alternatives,
    }: item_loader::Item,
) -> model::Item {
    model::Item {
        slug: slugify(&name),
        name,
        alternative_names,
        e_number,
        state,
        description,
        sources,
        vegan_alternatives,
    }
}
