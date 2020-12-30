#!/usr/bin/env bash

set -e

archive_name="grcov-linux-x86_64.tar.bz2"
download_url="https://github.com/mozilla/grcov/releases/download/v0.5.5/$archive_name"

cd $(mktemp -d)
wget "$download_url"
tar -xvf "$archive_name"
sudo mv grcov /usr/local/bin/
