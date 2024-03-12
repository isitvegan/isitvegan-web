#!/usr/bin/env python3

import json
import toml
from glob import glob
from os import path
import os

items_directory = path.join(path.dirname(__file__), "..", "..", "items")
build_dir = path.join(path.dirname(__file__), "..", "build")

items = [
    item
    for p in glob("**/*.toml", root_dir=items_directory, recursive=True)
    for item in toml.load(path.join(items_directory, p))["items"]
    if "e_number" in item
]

os.makedirs(build_dir, exist_ok=True)

with open(path.join(build_dir, "items.json"), "w+") as fp:
    json.dump(items, fp, indent=4)
