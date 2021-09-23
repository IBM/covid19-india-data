import sqlite3
from .db import DB


class TableOverview(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'Metadata_Tables_Overview'
        self.table_desc = 'A description of all the state tables there are in this database'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'table_name': 'STRING NOT NULL PRIMARY KEY',
            'state': 'STRING',
            'description': 'STRING'
        }
        return cols
