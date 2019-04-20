use url::Url;

pub struct Result {
    pub item: String,
    pub state: State,
    pub description: String,
    pub sources: Vec<Source>,
}

pub enum State {
    Yes,
    No,
    Possibly,
}

pub enum Source {
    Url(Url),
}
