import sqlite3
from .db import DB


class TestingTable(DB):

    def __init__(self):
        self.table_name = 'WB_testing'
        self.table_desc = 'West Bengal testing snapshot'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'samples_tested_today': 'INT',
            'total_samples_tested': 'INT',
            'positivity_rate': 'FLOAT',
            'tests_per_million': 'FLOAT',
            'n_testing_labs': 'INT',
            'rtpcr_antigen_ratio': 'FLOAT'
        }
        return cols
