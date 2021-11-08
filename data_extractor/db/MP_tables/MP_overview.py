import sqlite3
from .db import DB


class Overview(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_overview'
        self.table_desc = 'Overview'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'cases': 'INT',
        }
        return cols
