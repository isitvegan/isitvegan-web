#!/usr/bin/env python3

import json
import tomllib as toml
from glob import glob
from os import path
import os
import jq


def load_items(path):
    with open(path, "rb") as fp:
        return toml.load(fp)["items"]

def load_patches(path):
    with open(path, "rb") as fp:
        return toml.load(fp)["patch_item"]

def merge(left, right):
    if isinstance(left, dict) and isinstance(right, dict):
        return merge_dicts(left, right)
    if isinstance(left, list) and isinstance(right, list):
        return merge_lists(left, right)
    if type(left) == type(right):
        return right
    else:
        raise Exception("types do not match")

def merge_dicts(left: dict, right: dict):
    merged = {**left}
    for key, value in right.items():
        if key in merged:
            merged[key] = merge(merged[key], value)
        else:
            merged[key] = value
    return merged

def merge_lists(left: list, right: list):
    return [*left, *right]

def apply_patches(item, patches):
    for patch in patches:
        predicate = jq.compile(patch['if'])
        if predicate.input_value(item).first():
            item = merge(item, patch['patch'])
    return item

root_directory = path.join(path.dirname(__file__), "..", "..")
items_directory = path.join(root_directory, "items")
assert(path.exists(items_directory))
patches_directory = path.join(root_directory, "item-patches")
assert(path.exists(items_directory))
build_dir = path.join(root_directory, "build")

patches = load_patches(path.join(patches_directory, "e_numbers.toml"))
items = [
    apply_patches(item, patches)
    for p in glob("**/*.toml", root_dir=items_directory, recursive=True)
    for item in load_items(path.join(items_directory, p))
    if "e_number" in item
]
sorted_items = sorted(items, key=lambda item: (len(item["e_number"]), item["e_number"]))

os.makedirs(build_dir, exist_ok=True)

with open(path.join(build_dir, "items.json"), "w+") as fp:
    json.dump(sorted_items, fp, indent=4)
