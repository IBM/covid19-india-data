import sqlite3
from .db import DB


class PPEUnitTable(DB):

    def __init__(self):
        self.table_name = 'WB_equipment'
        self.table_desc = 'West Bengal protective gear equipment details'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'unit_name': 'STRING',
            'ppe': 'INT',
            'n95_masks': 'INT',
            'reusable_masks': 'INT',
            'disposable_masks': 'INT',
            'gloves': 'INT',
            'sanitizer': 'FLOAT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, unit_name))"
        return query