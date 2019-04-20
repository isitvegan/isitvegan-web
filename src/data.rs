use serde::{Deserialize, Serialize};
use url::Url;

#[derive(Serialize, Deserialize)]
pub struct Item {
    pub name: String,
    pub state: State,
    pub description: String,
    #[serde(default)]
    pub sources: Vec<Source>,
}

#[derive(Serialize, Deserialize)]
pub enum State {
    Yes,
    No,
    Possibly,
}

#[derive(Serialize, Deserialize)]
pub enum Source {
    #[serde(with = "url_serde")]
    Url(Url),
}
