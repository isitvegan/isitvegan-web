#!/usr/bin/env python3

import argparse
import subprocess

_LESS_FILE = 'less/main.less'
_CSS_FILE = 'build/main.css'

def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--release', action='store_true',
                        help='Build in release mode')
    return parser.parse_args()

def _run_lessc():
    subprocess.check_call(['lessc', _LESS_FILE, _CSS_FILE])

def _run_postcss():
    subprocess.check_call(['postcss', _CSS_FILE, '--replace'])

def build_css(release=False):
    _run_lessc()
    _run_postcss() if release else None


if __name__ == '__main__':
    arguments = _parse_arguments()
    build_css(arguments.release)
