from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import os
import sys
import pandas as pd
import sqlite3


def get_db_uri(db_fpath):
    uri = f'file:{db_fpath}?mode=ro'
    return uri


def get_tables(db_fpath):

    db_uri = get_db_uri(db_fpath)
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    con = sqlite3.connect(db_uri, uri=True)
    cursor = con.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    table_names = sorted([row[0] for row in records])
    con.close()
    return table_names


def read_table(table, conn):
    try:
        query = f'SELECT * FROM {table} ORDER BY date ASC;'
        df = pd.read_sql_query(query, conn)
    except:
        query = f'SELECT * FROM {table};'
        df = pd.read_sql_query(query, conn)
    
    return df


def export_tables_to_excel(db_fpath, output_fname, tables):

    wb = Workbook()
    db_uri =  get_db_uri(db_fpath)
    con = sqlite3.connect(db_uri, uri=True, isolation_level=None, 
                            detect_types=sqlite3.PARSE_COLNAMES)

    for idx, table in enumerate(sorted(tables)):
        sheet = wb.create_sheet(table[:31], index=idx)
        df = read_table(table, con)

        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)

    wb.save(output_fname)


def export_tables_to_csv(db_fpath, output_folder, tables):

    db_uri = get_db_uri(db_fpath)
    con = sqlite3.connect(db_uri, uri=True, isolation_level=None, 
                            detect_types=sqlite3.PARSE_COLNAMES)

    for table in sorted(tables):
        df = read_table(table, con)
        df.to_csv(os.path.join(output_folder, f'{table}.csv'), index=False)


def export_tables_to_json(db_fpath, output_folder, tables):

    db_uri = get_db_uri(db_fpath)
    con = sqlite3.connect(db_uri, uri=True, isolation_level=None, 
                            detect_types=sqlite3.PARSE_COLNAMES)

    for table in sorted(tables):
        df = read_table(table, con)
        df.to_json(os.path.join(output_folder, f'{table}.json'), orient='records')


def convert_db_to_other_formats(db_fpath, output_dir):

    tables = get_tables(db_fpath)
    fname_tables_dict = {}

    for tbl in tables:
        fname = tbl.split('_')[0]
        
        if fname not in fname_tables_dict:
            fname_tables_dict[fname] = []
        fname_tables_dict[fname].append(tbl)

    
    # Create excel files
    xls_outputdir = os.path.join(output_dir, 'xlsx')
    os.makedirs(xls_outputdir, exist_ok=True)

    for fname, tables in fname_tables_dict.items():
        output_fpath = os.path.join(xls_outputdir, fname + '.xlsx')
        export_tables_to_excel(db_fpath, output_fpath, tables)

    # Create csv files:
    csv_outputdir = os.path.join(output_dir, 'csv')
    os.makedirs(csv_outputdir, exist_ok=True)

    for fname, tables in fname_tables_dict.items():
        csv_fpath = os.path.join(csv_outputdir, fname)
        os.makedirs(csv_fpath, exist_ok=True)
        export_tables_to_csv(db_fpath, csv_fpath, tables)

    # Create json files:
    json_outputdir = os.path.join(output_dir, 'json')
    os.makedirs(json_outputdir, exist_ok=True)

    for fname, tables in fname_tables_dict.items():
        json_fpath = os.path.join(json_outputdir, fname)
        os.makedirs(json_fpath, exist_ok=True)
        export_tables_to_json(db_fpath, json_fpath, tables)


if __name__ == "__main__":

    db_fpath = sys.argv[1]
    output_dir = sys.argv[2]
    convert_db_to_other_formats(db_fpath, output_dir)
