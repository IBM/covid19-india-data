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


def export_tables_to_excel(db_fpath, output_fname, tables):

    wb = Workbook()
    db_uri =  get_db_uri(db_fpath)
    con = sqlite3.connect(db_uri, uri=True, isolation_level=None, 
                            detect_types=sqlite3.PARSE_COLNAMES)

    for idx, table in enumerate(sorted(tables)):
        sheet = wb.create_sheet(table, index=idx)

        query = f'SELECT * FROM {table};'
        df = pd.read_sql_query(query, con)

        for r in dataframe_to_rows(df, index=False, header=True):
            sheet.append(r)

    wb.save(output_fname)


def convert_db_to_excel(db_fpath, output_dir):

    tables = get_tables(db_fpath)
    fname_tables_dict = {}

    for tbl in tables:
        fname = tbl.split('_')[0]
        
        if fname not in fname_tables_dict:
            fname_tables_dict[fname] = []
        fname_tables_dict[fname].append(tbl)

    
    os.makedirs(output_dir, exist_ok=True)

    for fname, tables in fname_tables_dict.items():
        output_fpath = os.path.join(output_dir, fname + '.xlsx')
        export_tables_to_excel(db_fpath, output_fpath, tables)


if __name__ == "__main__":

    db_fpath = sys.argv[1]
    output_dir = sys.argv[2]
    convert_db_to_excel(db_fpath, output_dir)
