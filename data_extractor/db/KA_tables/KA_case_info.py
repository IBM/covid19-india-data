import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        self.table_name = 'KA_case_info'
        self.table_desc = 'Karnataka overall case, discharge, fatality info'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'discharged_new': 'INT',
            'discharged_total': 'INT',
            'cases_new': 'INT',
            'cases_active_new': 'INT',
            'deaths_new': 'INT',
            'deaths_total': 'INT',
            'cases_active_total': 'INT',
            'positivity_rate_percent': 'FLOAT',
            'fatality_rate_percent': 'FLOAT',
            'active_cases_icu': 'INT'
        }
        return cols
