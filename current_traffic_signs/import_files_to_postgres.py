from datapunt_processing import logger
from datapunt_processing.helpers.connections import psycopg_connection_string
import subprocess
import psycopg2
from psycopg2 import sql
import re
import os

logging = logger()


def move_coordinates_microstation():
    # Used MSLINK 9688 Noord to match offset mldnr : E06 with dgn vs access db
    local_coord = [-2023648.989000000059605, -1658091.672999999951571]
    global_coord = [123835.77100000000791624, 489390.68800000002374873]

    transformation = [global_coord[0] - local_coord[0], global_coord[1] - local_coord[1]]


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
    schema.replace('\r\n', ' ').replace('\n', ' ').replace('\r', '')  
    schema = re.sub(r'postgres_unknown 0x10', 'text', schema)
    schema = re.sub(r'index "([A-Za-z0-9-_]+)"."([A-Za-z0-9-_]+)"', 'index "\g<1>_\g<2>"', schema)
    schema = re.sub(r'constraint "([A-Za-z0-9-_]+)"."([A-Za-z0-9-_]+)"', 'constraint "\g<1>_\g<2>"', schema)
    schema = re.sub(r'create table "([A-Za-z0-9-_]+)"."([A-Za-z0-9-_]+)"', 'drop table if exists "\g<1>"."\g<2>";\ncreate table "\g<1>"."\g<2>"', schema)
    print(schema)
    return schema


def run_command_sync(cmd, allow_fail=False):
    '''run a shell command and return the command line output'''
    logging.info('Running %s', scrub(cmd))
    stdout = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE).communicate()[0].decode('latin1').split('\n')
    return stdout


def create_pg_schema(cursor, schema_name):
    cursor.execute(
        sql.SQL("DROP SCHEMA IF EXISTS {} CASCADE;\nCREATE SCHEMA IF NOT EXISTS {}")
        .format(sql.Identifier(schema_name),sql.Identifier(schema_name)),)
    logging.info('Created schema {}'.format(schema_name))


def pg_connection():
    pg_string = psycopg_connection_string('config.ini', 'dev')
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
    logging.info('Created tables')


def get_table_names(mdb_file):
    '''Get table names'''
    table_names = subprocess.Popen(
        ['mdb-tables', '-1', mdb_file],
        stdout=subprocess.PIPE).communicate()[0].decode('latin1')
    tables = table_names.strip().split('\n')
    logging.info('Tables: {}'.format(tables))
    return tables


def run_insert(text, cursor, schema_name):
        '''Prepare and run each insert statement
        Preparation is for case correction
        '''
        # regex for converting table and field names to lowercase
        expression = re.compile(r'INSERT INTO "{}"."([a-z_]+)" \((.*)\) VALUES'.format(schema_name))
        # replace table name with lower
        text = re.sub(expression, lambda x: x.group(0).lower(), text)
        # replace field name with lower
        text = re.sub(expression, lambda x: x.group(1).lower(), text)
        try:
            cursor.execute(text)
        except psycopg2.ProgrammingError as e:
            logging.info('Uh oh! ' + str(e)) #  + text)
        except psycopg2.IntegrityError as e:
            # thrown if there's a problem with duplicate primary keys or other
            # constraints
            logging.info('Uh oh! ' + str(e))


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
    for table in tables:
        if table != '':
            logging.info('Dumping ' + table + ' table...')
            command = [
                'mdb-export',
                '-I',
                'postgres',
                '-N'+schema_name,
                '-q'+'\'', # set quoting to single quote with values
                mdb_file,
                table.lower()]
            insert_statements = run_command_sync(command)
            [run_insert(line,
                        cursor,
                        schema_name)
             for line in insert_statements]


def create_geoms_repositioned(cursor, schema_name, table_name):
    cursor.execute(
        sql.SQL("""
        ALTER TABLE {}.{}
            ADD COLUMN xcoord_repositioned double precision,
            ADD COLUMN ycoord_repositioned double precision;
        ALTER TABLE {}.{} DROP COLUMN IF EXISTS geom;  
        SELECT AddGeometryColumn ({},{},'geom',28992,'POINT',2);

        UPDATE {}.{}
            SET xcoord_repositioned = xcoord+123835.77100000000791624+2023648.989000000059605,
            ycoord_repositioned = ycoord+489390.68800000002374873+1658091.672999999951571;
        UPDATE {}.{}
            SET geom =
            CASE
               WHEN
                  xcoord_repositioned is not null
               THEN
                  ST_PointFromText('POINT('||xcoord_repositioned||' '||ycoord_repositioned||')',28992)
               END""")
    .format(sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.Literal(schema_name),
            sql.Literal(table_name),
            sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.Identifier(schema_name),
            sql.Identifier(table_name)),)
    logging.info('added geometry column to {}'.format(table_name))


def create_geoms(cursor, schema_name, table_name):
    cursor.execute(
        sql.SQL("""
    ALTER TABLE {}.{} DROP COLUMN IF EXISTS geom;
    SELECT AddGeometryColumn ({},{},'geom',28992,'POINT',2);
    UPDATE {}.{}
    SET geom =
    CASE
       WHEN
          xcoord is not null
       THEN
          ST_PointFromText('POINT('||xcoord||' '||ycoord||')',28992)
       END""")
    .format(sql.Identifier(schema_name),
            sql.Identifier(table_name),
            sql.Literal(schema_name),
            sql.Literal(table_name),
            sql.Identifier(schema_name),
            sql.Identifier(table_name)),)
    logging.info('added geometry column to {}'.format(table_name))


def import_mdb(cursor, schema_name, mdb_file):
    create_pg_schema(
        cursor,
        schema_name)
    create_pg_tables(
        cursor,
        schema_name,
        mdb_file)
    dump_tables_to_db(cursor, mdb_file, None, schema_name)
    if schema_name == 'nieuw-west':
        create_geoms(cursor, schema_name, 'vm_gegevens')
    if schema_name in ('noord','west'):
        create_geoms_repositioned(cursor, schema_name, 'vm_gegevens')


def create_final_table(cursor):
    cursor.execute(sql.SQL("""
        DROP TABLE IF EXISTS current_traffic_signs;
        SELECT
            'Noord' as stadsdeel, mslink, mapid, bslnummer, mtrnummer, mdlnr, reflectie, bevestiging, 
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats, 
            datum_contr, xcoord_repositioned, ycoord_repositioned, datum_vervangen, straatnaam, straat_id, 
            wegvaknummer, rayon, opmerking, datum_vernieuw, x_brd, y_brd, 
            geom
        INTO current_traffic_signs
        FROM noord.vm_gegevens
        UNION ALL
        SELECT
            'West', mslink, mapid, bslnummer, mtrnummer, mdlnr, reflectie, bevestiging, 
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats, 
            datum_contr, xcoord_repositioned, ycoord_repositioned, datum_vervangen, straatnaam, straat_id, 
            wegvaknummer, rayon, opmerking, datum_vernieuw, x_brd, y_brd, 
            geom
        FROM west.vm_gegevens
        UNION ALL
        SELECT
            'Nieuw-West', mslink, mapid, bslnummer, mtrnummer, mdlnr, reflectie, bevestiging, 
            afmeting, status, onderbordmdlnr, onderbordtekst, datum_plaats,
            datum_contr, xcoord, ycoord, datum_vervangen, straatnaam, straat_id,
            wegvaknummer, rayon, opmerking, datum_vernieuw, x_brd, y_brd,
            geom
        FROM "nieuw-west".vm_gegevens;
        ALTER TABLE current_traffic_signs ADD COLUMN id SERIAL PRIMARY KEY;
        """))
    logging.info('Created table: current_traffic_signs')


def main():
    data_folder = '../data/'
    mdb_files = [
    {'schema': 'nieuw-west',
     'path': 'beheerassets/nieuw-west/verkeersborden_en_maatregelen_nieuwwest_1jul2014.mdb'},
    {'schema': 'noord',
     'path': 'beheerassets/noord/vm_stadsdeel_noord.mdb'},
    {'schema': 'west',
     'path': 'beheerassets/west/vm_sd_west2015.mdb'}
    ]

    cursor = pg_connection()
    for mdb_file in mdb_files:
        mdb_path = os.path.join(data_folder,mdb_file['path'])
        import_mdb(cursor, mdb_file['schema'], mdb_path)
    create_final_table(cursor)


if __name__ == "__main__":
    main()
