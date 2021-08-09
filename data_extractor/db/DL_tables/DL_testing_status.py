import sqlite3
from .db import DB


class TestingStatusTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_testing_status'
        self.table_desc = 'RTPCR / Rapid Antigen test information table for Delhi state'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'rtpcr_test_24h': 'INT',
            'antigen_test_24h': 'INT',
            'total_tests': 'INT',
            'tests_per_million': 'FLOAT'
        }
        return cols
