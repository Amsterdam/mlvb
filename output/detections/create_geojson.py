#!/usr/bin/env python3
"""
Convert classification results to GeoJSON.
"""
# By Amsterdam Datapunt
from __future__ import print_function

import argparse
import csv
import json

GEOMETRY_FIELDS = ['geometry', 'coordinates']


def read_csv(filename):
    """
    Process CSV of traffic sign classifications output GeoJSON.
    """
    features = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')

        # determine fieldname of geometry:
        geom_fieldname = 'geometry' if 'geometry' in reader.fieldnames else 'coordinates'

        next(reader) # skip header
        for chunks in reader:
            lon, lat = [float(x) for x in chunks[geom_fieldname].split()]
            features.append({
                'id': int(chunks['']),
                'properties': {
                    'pano_id': chunks['pano_id'],
                    'direction': int(chunks['direction']),
                },
                'geometry': {
                    'type': 'Point',
                    'coordinates': [lon, lat]
                },
                'type': 'Feature'
            })

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
        description='Convert traffic sign classification results from CSV to GeoJSON'
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
