#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# Get data
python download_from_objectstore.py config.ini objectstore beheerassets /data

