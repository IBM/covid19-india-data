import sqlite3
from .db import DB


class Testing(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_testing'
        self.table_desc = 'Advanced testing reports.'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'samples_sent': 'INT',
            'reports_received': 'INT',
            'reports_pending': 'INT',
            'positive_report': 'INT',
            'negative_report': 'INT',
        }
        return cols

