//! A useful tool to check wether food is vegan 🌱

#![type_length_limit = "2965010"]
#![warn(missing_docs, clippy::dbg_macro, clippy::unimplemented)]
#![deny(
    rust_2018_idioms,
    future_incompatible,
    missing_debug_implementations,
    clippy::doc_markdown,
    clippy::default_trait_access,
    clippy::enum_glob_use,
    clippy::needless_borrow,
    clippy::large_digit_groups,
    clippy::explicit_into_iter_loop
)]

#[macro_use]
extern crate rocket;

pub mod config_loader;
pub mod item_loader;
pub mod item_mapper;
pub mod item_packer;
pub mod model;
pub mod search_engine;
pub mod server;
