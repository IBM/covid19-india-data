import sqlite3
from .db import DB

class RailwaySurveillanceTable(DB):
    def __init__(self):
        self.table_name = "TN_Railway_surveillance"
        self.table_desc = "Tamil Nadu Railway station surveillance details till previous day, table number from the top last page"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIVATE KEY',
            'trains': 'INT',
            'passengers': 'INT',
            'negative': 'INT',
            'positive_cases': 'INT'
        }

        return cols
