#!/usr/bin/env python3.7

import argparse
import shutil
import os


def _parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target', action='store',
                        help='Target folder where files are copied to')
    return parser.parse_args()


def copy_files(target: str):
    shutil.copy('index.html', target)
    build_dir = os.path.join(target, 'build')
    if not os.path.exists(build_dir):
        os.makedirs(build_dir)
    shutil.copy('build/main.css', build_dir)
    shutil.copy('build/main.js', build_dir)


if __name__ == '__main__':
    arguments = _parse_arguments()
    copy_files(arguments.target)
