#!/usr/bin/env python3

import json
import tomllib as toml
from glob import glob
from os import path
import os


def load_items(path):
    with open(path, "rb") as fp:
        return toml.load(fp)["items"]


items_directory = path.join(path.dirname(__file__), "..", "items")
assert(path.exists(items_directory))
build_dir = path.join(path.dirname(__file__), "..", "build")

items = [
    item
    for p in glob("**/*.toml", root_dir=items_directory, recursive=True)
    for item in load_items(path.join(items_directory, p))
    if "e_number" in item
]
sorted_items = sorted(items, key=lambda item: (len(item["e_number"]), item["e_number"]))

os.makedirs(build_dir, exist_ok=True)

with open(path.join(build_dir, "items.json"), "w+") as fp:
    json.dump(sorted_items, fp, indent=4)
