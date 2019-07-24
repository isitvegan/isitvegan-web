//! Plain old data types

use chrono::{Date, Utc};
use serde::{Deserialize, Serialize};
use url::Url;

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

    /// A URL-friendly identifier for this item.
    pub slug: String,

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
pub struct Source {
    /// The date when this source was last checked.
    pub last_checked: Option<UtcDate>,
    /// The value of this source.
    #[serde(flatten)]
    pub kind: SourceKind,
}

/// Newtype
#[derive(Debug, Serialize, Deserialize)]
#[serde(transparent)]
pub struct UtcDate(#[serde(with = "serde_date_format")] Date<Utc>);

/// A source for an item's [`State`]
#[derive(Debug, Serialize, Deserialize)]
#[serde(tag = "type", content = "value")]
#[serde(rename_all = "camelCase")]
pub enum SourceKind {
    /// An online source
    #[serde(with = "url_serde")]
    Url(Url),
}

mod serde_date_format {
    use chrono::{Date, NaiveDate, Utc};
    use serde::{self, Deserialize, Deserializer, Serializer};

    const FORMAT: &'static str = "%Y-%m-%d";

    pub fn serialize<S>(date: &Date<Utc>, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: Serializer,
    {
        let s = format!("{}", date.format(FORMAT));
        serializer.serialize_str(&s)
    }

    pub fn deserialize<'de, D>(deserializer: D) -> Result<Date<Utc>, D::Error>
    where
        D: Deserializer<'de>,
    {
        let string = String::deserialize(deserializer)?;
        let naive_date =
            NaiveDate::parse_from_str(&string, FORMAT).map_err(serde::de::Error::custom)?;
        Ok(Date::from_utc(naive_date, Utc))
    }
}
