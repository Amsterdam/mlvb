#!/usr/bin/env python3
"""
Convert classification results to GeoJSON.
"""
# By Amsterdam Datapunt
from __future__ import print_function

import argparse
import csv
import json
import requests
import os

GEOMETRY_FIELDS = ['geometry', 'coordinates']


def read_csv(filename):
    """
    Process CSV of traffic sign classifications output GeoJSON.
    """
    features = []
    base_url = 'https://api.data.amsterdam.nl/panorama/recente_opnames/alle/'

    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')

        # determine fieldname of geometry:
        geom_fieldname = 'geometry' if 'geometry' in reader.fieldnames else 'coordinates'

        next(reader) # skip header
        for chunks in reader:
            # lon, lat = [float(x) for x in chunks[geom_fieldname].split()]
            uri = os.path.join(base_url, chunks['pano_id'])
            pano_uri = requests.get(uri)
            pano_json = pano_uri.json()
            features.append({
                'id': int(chunks['']),
                'properties': {
                    'pano_id': chunks['pano_id'],
                    'direction': int(chunks['direction']),
                    'url': pano_json['image_sets']['equirectangular']['small']
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [chunks['x'], chunks['y']]
                },
                'type': 'Feature'
            })
            print()

    return {
        'type': 'FeatureCollection',
        'features': features,
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'epsg:4326'
            }
        }
    }


def handle_cli():
    """
    Handle the commandline.
    """
    parser = argparse.ArgumentParser(
        description="""
        Convert traffic sign classification results from CSV to GeoJSON 
        and adding url small image urls via api.data.amsterdam.nl, like:
        https://data.amsterdam.nl/panorama/2017/03/07/TMX7316010203-000198/pano_0000_000000/equirectangular/panorama_2000.jpg
        from id TMX7316010203-000301_pano_0000_003409

        Example:
        ` python create_geojson.py --csv locations-detected-2018-05-15.csv --geojson 2018-05-15-detections-vluchtheuvel-bakens.json python create_geojson.py --csv locations-detected-2018-05-15.csv --geojson 2018-05-15-detections-vluchtheuvel-bakens.json`
        """
    )
    parser.add_argument(
        '--csv',
        help='path to CSV file with detections and coordinates',
        type=str,
        required=True
    )
    parser.add_argument(
        '--geojson',
        help='path to GeoJSON file that should be written',
        type=str,
        required=True
    )

    return parser.parse_args()


def main():
    """
    entrypoint
    """
    arguments = handle_cli()

    print('Reading CSV input:', arguments.csv)
    json_data = read_csv(arguments.csv)

    print('Writing GeoJSON output', arguments.geojson)
    with open(arguments.geojson, 'w') as f_out:
        json.dump(json_data, f_out)


if __name__ == '__main__':
    main()
