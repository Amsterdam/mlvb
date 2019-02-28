from datapunt_processing import logger
from datapunt_processing.helpers.connections import psycopg_connection_string
from datapunt_processing.helpers.files import create_dir_if_not_exists
from datapunt_processing.helpers.connections import postgres_engine_pandas

import argparse
import subprocess
import psycopg2
from psycopg2 import sql
import re
import os
import sys
import glob
import pandas as pd

logger = logger()


class NonZeroReturnCode(Exception):
    pass


def scrub(l):
    out = []
    for x in l:
        if x.strip().startswith('PG:'):
            out.append('PG: <CONNECTION STRING REDACTED>')
        else:
            out.append(x)
    return out


def cleanup_table_create(schema):
    '''
    Clean table create statements to fix naming errors and replace actions.
    '''
    schema = "\n".join(schema).lower()
    schema = re.sub(r'varchar \(\d+\)', 'text', schema) # char var gives errors with long text fields
    schema = re.sub(r'postgres_unknown 0x10', 'text', schema)
    schema = re.sub(r'index "([A-Za-z0-9-_]+)"."([A-Za-z0-9-_~]+)"', 'index "\g<1>_\g<2>"', schema)
    schema = re.sub(r'constraint "([A-Za-z0-9-_]+)"."([A-Za-z0-9-_]+)"', 'constraint "\g<1>_\g<2>"', schema)
    schema = re.sub(r'create table "([A-Za-z0-9-_]+)"."([A-Za-z0-9-_]+)"', 'drop table if exists "\g<1>"."\g<2>";\ncreate table "\g<1>"."\g<2>"', schema)
    schema = re.sub(r'unique', '', schema)  # remove unique constriant, else errors when importing
    print(schema)
    return schema


def run_command_sync(cmd, allow_fail=False):
    '''run a shell command and return the command line output'''
    encoding = sys.stdout.encoding
    logger.info('Running %s', scrub(cmd))
    stdout = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE).communicate()[0].replace(b'\r',b'').decode(encoding).splitlines()
    return stdout


def create_pg_schema(cursor, schema_name):
    cursor.execute(
        sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE;\nCREATE SCHEMA IF NOT EXISTS {}")
        .format(sql.Identifier(schema_name),sql.Identifier(schema_name)),)
    logger.info('Created schema {}'.format(schema_name))


def pg_connection(config_path, config_name):
    pg_string = psycopg_connection_string(config_path, config_name)
    connection = psycopg2.connect(pg_string)
    connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    return cursor


def create_pg_tables(cursor, schema_name, mdb_file):
    """
    Example command:
    mdb-schema -Nnoord ../data/beheerassets/noord/vm_stadsdeel_noord.mdb postgres
    """
    cmd = ['mdb-schema', '-N'+schema_name, mdb_file, 'postgres']
    get_tables_from_mdb = run_command_sync(cmd)
    schema = cleanup_table_create(get_tables_from_mdb)
    cursor.execute(schema)
    print(schema)
    logger.info('Created tables')


def get_table_names(mdb_file):
    '''Get table names'''
    table_names = subprocess.Popen(
        ['mdb-tables', '-1', mdb_file],
        stdout=subprocess.PIPE).communicate()[0].decode('utf-8')
    tables = table_names.strip().split('\n')
    logger.info('Tables: {}'.format(tables))
    return tables


def run_insert(text, cursor, schema_name):
        '''Prepare and run each insert statement
           Preparation is for case correction
        '''
        # regex for converting table and field names to lowercase
        expression = re.compile(r'\(([A-Za-z0-9_\-\s\,\"]+)\) VALUES')
        # replace field name with lowercase
        text = re.sub(expression, lambda x: x.group(0).lower(), text)
        # replace empty date fields with NULL
        text = re.sub(r"'__-__-____'", r'NULL', text)
        text = re.sub(r"'__-__-____'", r'NULL', text)
        try:
            #text = cursor.mogrify(text)
            #text = cursor.mogrify(text).replace(b'\r\n',b'')
            #print(text)
            cursor.execute(text)
        except psycopg2.ProgrammingError as e:
            logger.info('Error ' + str(e))
        except psycopg2.IntegrityError as e:
            logger.info('Problem with duplicate primary keys or constraints: ' + str(e))


def dump_tables_to_db(cursor, mdb_file, table_names, schema_name):
    '''Dump each table in mdb to sql file
       Commandline TEST:
       mdb-export -I postgres -Nnoord ../data/beheerassets/noord/vm_stadsdeel_noord.mdb VM_GEGEVENS
    '''
    if table_names is None:
        tables = get_table_names(mdb_file)
    else:
        tables = table_names.split(',')
        print(tables)
    sql_dir_name = 'sql_inserts'
    create_dir_if_not_exists(sql_dir_name)

    for table in tables:
        if table != '':
            logger.info('Dumping ' + table + ' table...')
            command = [
                'mdb-export',
                '-I',
                'postgres',
                '-N'+schema_name,
                '-q'+'\'',  # set quoting to single quote with values
                mdb_file,
                table.lower()]
            insert_sql_statements = run_command_sync(command)
            file_name = os.path.join(sql_dir_name, schema_name+'_'+table+'.sql')

            with open(file_name, 'w', newline="\n") as a:
                a.writelines(insert_sql_statements)

            with open(file_name, 'r') as insert_statements:
                [run_insert(line,
                            cursor,
                            schema_name)
                 for line in insert_statements]


def create_geoms(cursor, schema_name, table_name, x_name, y_name):
    cursor.execute(
        sql.SQL("""
    ALTER TABLE {0}.{1} DROP COLUMN IF EXISTS geom;
    SELECT AddGeometryColumn ({2},{3},'geom',28992,'POINT',2);
    UPDATE {0}.{1}
    SET geom =
       CASE
          -- FIX Microstation offset. Used MSLINK 9688 Noord to match offset mldnr : E06 with dgn vs access db
          WHEN {4} is not null and {4} < 100000 THEN
            ST_PointFromText('POINT('||{4}+123835.77100000000791624+2023648.989000000059605||' '||{5}+489390.68800000002374873+1658091.672999999951571||')',28992)
          WHEN {4} is not null and {4} > 100000 THEN
            ST_PointFromText('POINT('||{4}||' '||{5}||')',28992)
       END""").format(sql.Identifier(schema_name),
                      sql.Identifier(table_name),
                      sql.Literal(schema_name),
                      sql.Literal(table_name),
                      sql.Identifier(x_name),
                      sql.Identifier(y_name)),)
    logger.info('added geometry column to {}'.format(table_name))


def import_mdb(cursor, schema_name, mdb_file):
    create_pg_schema(
        cursor,
        schema_name)
    create_pg_tables(
        cursor,
        schema_name,
        mdb_file)
    dump_tables_to_db(cursor, mdb_file, None, schema_name)
    create_geoms(cursor, schema_name, 'vm_gegevens', 'xcoord', 'ycoord')


def create_final_table(cursor):
    cursor.execute(sql.SQL("""
        DROP TABLE IF EXISTS current_traffic_signs;
        SELECT
            'Noord' as stadsdeel, LEFT(mdlnr,3) as bord_code, mslink, mapid, mdlnr, reflectie, bevestiging, 
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats, 
            datum_contr, datum_vervangen, straatnaam, straat_id, 
            wegvaknummer, rayon, opmerking, datum_vernieuw, xcoord, ycoord, 
            geom
        INTO current_traffic_signs
        FROM noord.vm_gegevens
        UNION ALL
        SELECT
            'West', LEFT(mdlnr,3), mslink, mapid, mdlnr, reflectie, bevestiging,
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
            datum_contr, datum_vervangen, straatnaam, straat_id,
            wegvaknummer, rayon, opmerking, datum_vernieuw, xcoord, ycoord,
            geom
        FROM west.vm_gegevens
        UNION ALL
        SELECT
            'Nieuw-West', LEFT(mdlnr,3), mslink, mapid, mdlnr, reflectie, bevestiging,
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
            datum_contr, datum_vervangen, straatnaam, straat_id,
            wegvaknummer, rayon, opmerking, datum_vernieuw, xcoord, ycoord,
            geom
        FROM "nieuw-west".vm_gegevens
        UNION ALL
        SELECT
            'Zuid', LEFT(mdlnr,3), mslink, mapid, mdlnr, reflectie, bevestiging,
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
            datum_contr,datum_vervangen, straatnaam, straat_id,
            wegvaknummer, rayon, opmerking, datum_vernieuw, xcoord, ycoord, 
            geom
        FROM "zuid".vm_gegevens
        UNION ALL
        SELECT
            'Oost', LEFT(mdlnr,3), mslink, mapid, mdlnr, reflectie, bevestiging,
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
            datum_contr, datum_vervangen, straatnaam, straat_id,
            wegvaknummer, rayon, opmerking, datum_vernieuw, xcoord, ycoord,
            geom
        FROM "oost".vm_gegevens
        UNION ALL
        SELECT
            'Centrum', LEFT(ebtype,3), ogc_fid, elementid, ebtype, ebreflecti, ebbevestig,
            ebgrootte, ebigebrekb, NULL, ebtekstopb, ebjaarplaa,
            eiinspecti::text, NULL, elstraat, NULL,
            NULL, elwijk, ebiopmerki, NULL, elxcoord, elycoord,
            wkb_geometry
        FROM centrum.amsterdam_vbpoint
        UNION ALL
        SELECT
            'Zuidoost', LEFT("type bord",3), index, uid_drager, "type bord", reflectieklasse, bevestigingstype,
            grootte, status_i,onderbord,tekst_bord, productiejaar,
            NULL, NULL, drager_straat, NULL,
            NULL, NULL, opmerkingen, NULL,"x-coordinaat", "y-coordinaat",
            geom
        FROM zuidoost.verkeersborden_zo;
        ALTER TABLE current_traffic_signs ADD COLUMN id SERIAL PRIMARY KEY;"""))
    logger.info('Created table: current_traffic_signs')


def import_shapefiles(cursor, pg_string, data_folder, shp_dirs):
    for shp_dir in shp_dirs:
        create_pg_schema(cursor, shp_dir['schema'])
        full_path = os.path.join(data_folder, shp_dir['path'], "*.shp")
        for shp_filename in glob.glob(full_path):
            logger.info('Found: '+shp_filename+', saving to Postgres')
            shp2psql(shp_filename, pg_string, shp_filename.split('/')[-1][:-4], shp_dir['schema'])
            cursor.close()


def shp2psql(shp_filename, pg_string, layer_name, schema_name):
    cmd = [
        'ogr2ogr', '-nln', schema_name+'.'+layer_name, '-lco','precision=NO', '-F', 'PostgreSQL',
        'PG:'+pg_string, shp_filename
    ]
    stdout = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE, env={**os.environ, 'PGCLIENTENCODING':'LATIN-1'})  # UTF-8 gives encoding error


def load_xls(cursor, datadir, schema_name, config_path, config_name):
    """Load xlsx into postgres for multiple files"""
    files = os.listdir(datadir)
    files_xls = [f for f in files if f.split('.')[-1] in ('xlsx', 'xls')]
    logger.info(files_xls)

    for filename in files_xls:
        df = pd.read_excel(datadir + '/' + filename, skiprows=1)
        if df.empty:
            logger.info('No data')
            continue
        df.columns = map(str.lower, df.columns)
        logger.info("added " + filename)
        logger.info(df.columns)

        # load the data into pg
        engine = postgres_engine_pandas(config_path, config_name)
        table_name = filename.split('.')[0]
        create_pg_schema(cursor, schema_name)
        df.to_sql(table_name, engine, schema=schema_name, if_exists='replace')  # ,dtype={geom: Geometry('POINT', srid='4326')})
        logger.info(filename + ' added as ' + table_name)
        create_geoms(cursor, schema_name, table_name,'x-coordinaat','y-coordinaat')
        cursor.execute(sql.SQL("""ALTER TABLE {}.{} ADD COLUMN id SERIAL PRIMARY KEY;""")
                       .format(sql.Identifier(schema_name),
                               sql.Identifier(table_name)),)


def save_geojson(cursor, pg_string, table_name, output_folder):
    create_dir_if_not_exists(output_folder)
    full_path = os.path.join(output_folder,table_name+'.geojson')
    cmd = [
        'ogr2ogr', '-F', 'GeoJSON', full_path,
        'PG:'+pg_string, table_name
    ]
    stdout = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE)
    logger.info("Writen GeoJSON to: {}".format(full_path))


def parser():
    """Parser function to run arguments from commandline and to add description to sphinx docs."""
    description = """
    Use docker or local setup to import files:
    ``python import_files_to_postgres.py config.ini docker``

    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('config_path',
                        type=str,
                        help="Full Location of config.ini file")
    parser.add_argument('config_name',
                        type=str,
                        help="Define the running env: 'docker' or 'dev' when running locally")
    return parser


def main():
    args = parser().parse_args()
    pg_string = psycopg_connection_string(args.config_path, args.config_name)
    cursor = pg_connection(args.config_path, args.config_name)

    data_folder = '../data/'

    mdb_files = [
        {'schema': 'nieuw-west',
         'path': 'beheerassets/nieuw-west/verkeersborden_en_maatregelen_nieuwwest_1jul2014.mdb'},
        {'schema': 'noord',
         'path': 'beheerassets/noord/vm_stadsdeel_noord.mdb'},
        {'schema': 'west',
         'path': 'beheerassets/west/vm_sd_west2015.mdb'},
        {'schema': 'oost',
         'path': 'beheerassets/oost/vm_stadsdeel_oost.mdb'},
        {'schema': 'zuid',
         'path': 'beheerassets/zuid/vm_zuid_verouderde_gegevens.mdb'},
        ]
    for mdb_file in mdb_files:
        mdb_path = os.path.join(data_folder,mdb_file['path'])
        import_mdb(cursor, mdb_file['schema'], mdb_path)

    shp_files = [
        {'schema': 'centrum',
         'path': 'beheerassets/centrum'},
        {'schema': 'amsterdamse_bos',
         'path': 'beheerassets/adam_bos'}
        ]
    import_shapefiles(cursor, pg_string, data_folder, shp_files)

    xls_files = [
        {'schema': 'zuidoost',
         'path': 'beheerassets/zuidoost'}
        ]
    load_xls(cursor, os.path.join(data_folder, xls_files[0]['path']), xls_files[0]['schema'], args.config_path, args.config_name)

    create_final_table(cursor)
    save_geojson(cursor, 'current_traffic_signs', '../output')


if __name__ == "__main__":
    main()
