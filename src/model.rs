//! Plain old data types

use serde::{Deserialize, Serialize};
use url::Url;

/// The description of an item.
#[derive(Debug, Serialize, Deserialize)]
pub struct Item {
    /// The item's name or title.
    pub name: String,

    /// Alternative valid names for this item.
    pub alternative_names: Vec<String>,

    /// [E numbers] assigned to this item.
    ///
    /// [E numbers](https://en.wikipedia.org/wiki/E_number)
    pub e_numbers: Vec<u16>,

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

/// The vegan-ness of an item.
#[derive(Debug, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub enum State {
    /// The item is definitely or overwhelmingly typically vegan.
    Vegan,

    /// The item is probably not vegan
    Carnist,

    /// The item could be vegan, depending on how it was produced
    ItDepends,
}

/// A source for an item's [`State`]
#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "type", content = "value")]
#[serde(rename_all = "camelCase")]
pub enum Source {
    /// An online source
    #[serde(with = "url_serde")]
    Url(Url),
}
