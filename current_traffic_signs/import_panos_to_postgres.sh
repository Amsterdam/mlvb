#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# Import data
python load_wfs_to_postgres.py config.ini docker https://map.data.amsterdam.nl/maps/panorama panorama_recent_2017 28992 
