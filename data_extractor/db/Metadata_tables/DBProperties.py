import sqlite3
from .db import DB


class DBProperties(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'Metadata_DB_Properties'
        self.table_desc = 'Tracks key metadata for the database'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'key': 'STRING NOT NULL PRIMARY KEY',
            'value': 'STRING'
        }
        return cols

    def insert_row(self, cursor, **kwargs):

        cols = list(self.cols.keys())
        vals = [kwargs.get(col, None) for col in cols]
        colstr = ', '.join(cols)
        valstr = ', '.join(['?'] * len(cols))

        query = f'INSERT OR REPLACE INTO `{self.table_name}` ({colstr}) VALUES ({valstr})'
        cursor.execute(query, vals)
