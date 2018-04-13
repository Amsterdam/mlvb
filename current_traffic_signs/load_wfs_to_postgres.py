#!/usr/bin/env python3

import subprocess
import argparse
from urllib.parse import urlencode
import psycopg2
import requests
from psycopg2 import sql
from datapunt_processing import logger
from datapunt_processing.helpers.connections import psycopg_connection_string
# Setup basic logging
logger = logger()


class NonZeroReturnCode(Exception):
    """Used for subprocess error messages."""
    pass


def scrub(line):
    """Hide the login credentials of Postgres in the console."""
    out = []
    for x in line:
        if x.strip().startswith('PG:'):
            out.append('PG: <CONNECTION STRING REDACTED>')
        else:
            out.append(x)
    return out


def run_command_sync(cmd, retries=3):
    """
    Run a string in the command line.

    Args:
        1. cmd: command line code formatted as a list::

            ['ogr2ogr', '-overwrite', '-t_srs', 'EPSG:28992','-nln',layer_name,'-F' ,'PostgreSQL' ,pg_str ,url]

        2. Optional: allow_fail: True or false to return error code

    Returns:
        Excuted program or error message.
    """
    # logger.info('Running %s', scrub(cmd))
    retry = 0
    while retry < retries:
        p = subprocess.Popen(cmd)
        p.wait()
        if p.returncode != 0:
            retry += 1
        else:
            # status 200. succes.
            break
    if p.returncode != 0:
        raise NonZeroReturnCode
    return p.returncode


def pg_connection():
    pg_string = psycopg_connection_string('config.ini', 'dev')
    connection = psycopg2.connect(pg_string)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    return cursor


def remove_table(table_name):
    cursor = pg_connection()
    cursor.execute(sql.SQL("""
        DROP TABLE IF EXISTS {};""").format(sql.Identifier(table_name)),)


def get_number_of_records(url_api):
    url = requests.get(url_api)
    data = url.json()
    return data["count"]


def load_wfs_layer_into_postgres(pg_str, url_wfs, layer_name, srs, retry_count=3):
    """
    Get layer from a wfs service.
    Args:
        1. url_wfs: full url of the WFS including https, excluding /?::

            https://map.data.amsterdam.nl/maps/gebieden

        2. layer_name: Title of the layer::

            stadsdeel

        3. srs: coordinate system number, excluding EPSG::

            28992

    Returns:
        The layer loaded into postgres
    """  # noqa

    number_of_records = get_number_of_records("https://api.data.amsterdam.nl/panorama/recente_opnames/2017/")
    pages = round(number_of_records/10000)

    page = 1
    srs = "EPSG:{}".format(srs)
    while page <= pages:
        parameters = {
            "REQUEST": "GetFeature",
            "TYPENAME": layer_name,
            "SERVICE": "WFS",
            "VERSION": "2.0.0",
            "MAXFEATURES": 10000,
            "INDEX": page * 10000
            #"SRSNAME": "EPSG:{}".format(srs)
        }
        logger.info("Requesting data from {}, layer: {}, page: {} of {}".format(
            url_wfs, layer_name, page, pages))
        url = url_wfs + '?' + urlencode(parameters)
        cmd = ['ogr2ogr', '-append', '-t_srs', srs, '-nln', layer_name, '-F', 'PostgreSQL', 'PG:'+pg_str, url]
        run_command_sync(cmd)
        page +=1

def load_wfs_layers_into_postgres(config_path, db_config, url_wfs, layer_names, srs_name):
    """
    Load layers into Postgres using a list of titles of each layer within the WFS service.

    Args:
        pg_str: psycopg2 connection string::

        'PG:host= port= user= dbname= password='

    Returns:
        Loaded layers into postgres using ogr2ogr.

    """
    pg_str = psycopg_connection_string(config_path, db_config)

    layers = layer_names.split(',')
    logger.info('Layers:',layers)

    for layer_name in layers:
        remove_table(layer_name)
        load_wfs_layer_into_postgres(pg_str, url_wfs, layer_name, srs_name)
        logger.info(layer_name + ' loaded into PG.')


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx."""
    desc = """
    Upload gebieden into PostgreSQL from the WFS service with use of ogr2ogr.

    Add ogr2ogr path ENV if running locally in a virtual environment:
        ``export PATH=/Library/Frameworks/GDAL.framework/Programs:$PATH``

    Example command line:
        ``load_wfs_to_postgres config.ini dev https://map.data.amsterdam.nl/maps/gebieden 
          stadsdeel,buurtcombinatie,gebiedsgerichtwerken,buurt 28992``
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'config_path',
        type=str,
        help="Type the relative path + name of the config file, for example: auth/config.ini")
    parser.add_argument(
        'db_config',
        type=str,
        help="Type 'dev' or 'docker' to load the proper port and ip settings in the config file")
    parser.add_argument(
        'url',
        type=str,
        help="""
        Url of the WFS service, for example:
        https://map.data.amsterdam.nl/maps/gebieden
        """)
    parser.add_argument(
        'layers',
        type=str,
        help="""
        Name of the layers, for example
        stadsdeel,buurtcombinatie
        """)
    parser.add_argument(
        "srs",
        type=str,
        default="28992",
        choices=["28992", "4326"],
        help="choose srs (default: %(default)s)")
    return parser


def main():
    args = parser().parse_args()
    load_wfs_layers_into_postgres(
        args.config_path, args.db_config, args.url, args.layers, args.srs)


if __name__ == '__main__':
    main()
