#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error
set -x

# Set path to ogr2ogr on OSX
export PATH=/Library/Frameworks/GDAL.framework/Programs:$PATH

# Get data
python download_from_objectstore.py config.ini objectstore beheerassets ../data

# Import files to Postgres
python import_files_to_postgres.py

# Import pano xy and uri's from 2017
python load_wfs_to_postgres.py config.ini dev https://map.data.amsterdam.nl/maps/panorama panorama_recent_2017 28992 

# Create nearest pano table and export to csv
python select_nearest_panos.py config.ini dev D02ro_BB22 Gele\ koker ../output
python select_nearest_panos.py config.ini dev C02 Scharnierbeugel,Klemband,Overig ../output csv

python select_nearest_panos.py config.ini dev E06 Scharnierbeugel,Klemband,Overig,Lichtmast,390\ flessenpaal,360\ flessenpaal,Flessenpaal\ 360,Flessenpaal\ 390,Buispaal ../output csv

python select_nearest_panos.py config.ini dev C02 Scharnierbeugel,Klemband,Overig ../output json

python select_nearest_panos.py config.ini dev E06 Scharnierbeugel,Klemband,Overig,Lichtmast,390\ flessenpaal,360\ flessenpaal,Flessenpaal\ 360,Flessenpaal\ 390,Buispaal ../output json
