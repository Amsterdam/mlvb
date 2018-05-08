from datapunt_processing.helpers.logging import logger
from datapunt_processing.helpers.connections import psycopg_connection_string
from datapunt_processing.extract.write_table_to_csv import export_table_to_csv
from write_table_to_geojson import write_table_to_geojson
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


def list_to_pgarray(alist):
    return "','".join(alist)

def select_nearest_pano_by_sign(traffic_sign_code, fixation, outputformat):
    table_output_name = "nearest_panos_{}_{}".format(
        traffic_sign_code.lower(),
        fixation.split(',')[0].replace(' ', '_').lower())
    
    fixations = fixation.split(',')

    print(fixations)
    cursor = pg_connection()
    if outputformat == 'json':
        cursor.execute(sql.SQL("""
            DROP TABLE IF EXISTS {0};
            SELECT DISTINCT ON (c.id)
                c.id,
                c.stadsdeel,
                c.mdlnr,
                c.mslink,
                d.id as pano_id,
                REPLACE(d.url,'8000','2000') as url,
                ST_Transform(c.geom,4326) as geom
            INTO {0}
            FROM
                public.panorama_recent_2017 as d,
                (SELECT DISTINCT
                    id, stadsdeel, bord_code, mslink, mapid, mdlnr, reflectie, bevestiging,
                    afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
                    datum_contr, datum_vervangen, wegvaknummer,
                    opmerking, datum_vernieuw,
                    ST_X(ST_TRANSFORM(geom,4326)) as lat,
                    ST_Y(ST_TRANSFORM(geom,4326)) as lon,
                    geom
                 FROM
                    public.current_traffic_signs
                 WHERE "bord_code" = {1}) as c
            WHERE ST_CONTAINS(ST_BUFFER(c.geom, 6), d.wkb_geometry)""").format(
            sql.Identifier(table_output_name),
            sql.Literal(traffic_sign_code)),)
    if outputformat == 'csv':
        cursor.execute(sql.SQL("""
            DROP TABLE IF EXISTS {0};
            SELECT DISTINCT ON (c.id)
                d.*
            INTO {0}
            FROM
                public.panorama_recent_2017 as d,
                (SELECT DISTINCT
                    id, stadsdeel, bord_code, mslink, mapid, mdlnr, reflectie, bevestiging,
                    afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
                    datum_contr, datum_vervangen, wegvaknummer,
                    opmerking, datum_vernieuw,
                    ST_X(ST_TRANSFORM(geom,4326)) as lat,
                    ST_Y(ST_TRANSFORM(geom,4326)) as lon,
                    geom
                 FROM
                    public.current_traffic_signs
                 WHERE "bord_code" = {1}) as c
            WHERE ST_CONTAINS(ST_BUFFER(c.geom, 6), d.wkb_geometry)""").format(
            sql.Identifier(table_output_name),
            sql.Literal(traffic_sign_code)),)



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
    CSV outputs only the pano data, JSON outputs the registered traffic sign and the url to the pano view.

    Example command line:
        ``python select_nearest_panos.py config.ini dev D02 Gele\ koker,Scharnierbeugel ../output csv``

    Result:
        Table: nearest_panos_d02ro_bb22_gele_koker_yyyy-mm-dd.csv
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
    parser.add_argument('format',
                        type=str,
                        help='Define output format for example json or csv')
    return parser


def main():
    args = parser().parse_args()
    table = select_nearest_pano_by_sign(args.traffic_sign_code, args.fixation, args.format)
    if args.format == 'json':
        write_table_to_geojson(
            args.full_config_path,
            args.db_config, table,
            args.output_folder)
    if args.format == 'csv':
        export_table_to_csv(
            args.full_config_path,
            args.db_config, table,
            args.output_folder)
    logger.info("Written {}/{}.{}".format(args.output_folder, table, args.format))


if __name__ == "__main__":
    main()
