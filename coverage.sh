#!/usr/bin/env bash

set -e

zip -0 coverage.zip `find . \( -name '*is_it_vegan*.gc*' \) -print`
grcov coverage.zip \
       -t lcov \
       --llvm \
       --branch \
       --ignore-not-existing \
       --ignore '/*' \
       > lcov.info
