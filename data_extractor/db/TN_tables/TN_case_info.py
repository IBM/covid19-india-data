import sqlite3
from .db import DB

class CumulativeInfoTable(DB):
    def __init__(self):
        self.table_name = "TN_cumulative_info"
        self.table_desc = "Tamil Nadu cumulative info, table 1 on page 1 of bulletin"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'testing_facilities': 'INT',
            'government_testing_facilities': 'INT',
            'private_testing_facilities': 'INT',
            'active_cases_yesterday': 'INT',
            'positive_tested_cases': 'INT',
            'discharged_patients': 'INT',
            'deaths_today': 'INT',
            'active_cases_today': 'INT'
        }

        return cols
