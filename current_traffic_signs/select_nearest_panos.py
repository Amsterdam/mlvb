from datapunt_processing.helpers.logging import logger
from datapunt_processing.helpers.connections import psycopg_connection_string
from datapunt_processing.extract.write_table_to_csv import export_table_to_csv
from psycopg2 import sql
import argparse
import psycopg2

logger = logger()

def pg_connection():
    pg_string = psycopg_connection_string('config.ini', 'dev')
    connection = psycopg2.connect(pg_string)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    return cursor


def select_nearest_pano_by_sign(traffic_sign_code, fixation):
    table_output_name = "nearest_panos_{}_{}".format(traffic_sign_code.lower(), fixation.replace(' ', '_').lower())
    cursor = pg_connection()

    cursor.execute(sql.SQL("""
        DROP TABLE IF EXISTS {0};
        SELECT DISTINCT
            d.*
        INTO {0}
        FROM
            public.panorama_recent_2017 as d,
            (SELECT
                id,
                geom
             FROM
                public.current_traffic_signs
             WHERE "mdlnr" = {1} AND "bevestiging" = {2}) as c
        WHERE ST_CONTAINS(ST_BUFFER(c.geom, 6), d.wkb_geometry)""").format(
        sql.Identifier(table_output_name),
        sql.Literal(traffic_sign_code),
        sql.Literal(fixation)),)

    #pg_str = psycopg_connection_string
    #execute_sql(pg_str, sql_select_panos)
    return table_output_name


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Select the nearest pano images of a specific traffic sign, save them as a table and output them as a csv file.

    Example command line:
        ``python select_nearest_panos.py config.ini dev D02ro_BB22 Gele\ koker ../output``

    Result:
        Table: nearest_panos_d02ro_bb22_gele_koker
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('full_config_path',
                        type=str,
                        help='Location of the config file, for example config.ini')
    parser.add_argument('db_config',
                        type=str,
                        help='database config setting, for example dev or docker')
    parser.add_argument('traffic_sign_code',
                        type=str,
                        help='Write the selected traffic sign code, for example: D02_ro_22')
    parser.add_argument('fixation',
                        type=str,
                        help='Specify the fixation, for example: Gele koker')
    parser.add_argument('output_folder',
                        type=str,
                        help='Define output folder for example ../output')
    return parser


def main():
    args = parser().parse_args()
    table = select_nearest_pano_by_sign(args.traffic_sign_code, args.fixation)
    export_table_to_csv(args.full_config_path, args.db_config, table, args.output_folder)
    logger.info("Written {}/{}.csv".format(args.output_folder, table))

if __name__ == "__main__":
    main()
