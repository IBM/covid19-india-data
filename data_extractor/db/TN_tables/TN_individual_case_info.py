import sqlite3
from .db import DB

class CumulativeInfoTable(DB):
    def __init__(self):
        self.table_name = "TN_individual_case_info"
        self.table_desc = "Individual case information"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
        }

        return cols
