#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# Get data
python download_from_objectstore.py config.ini objectstore beheerassets /data

# Import files to Postgres
python import_files_to_postgres.py config.ini docker

# Import pano xy and uri's from 2017
# python load_wfs_to_postgres.py config.ini docker https://map.data.amsterdam.nl/maps/panorama panorama_recent_2017 28992

