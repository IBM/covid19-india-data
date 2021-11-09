import sqlite3
from .db import DB


class CaseInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MH_case_info'
        self.table_desc = 'Maharashtra daily new cases information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'discharged_today': 'INT',
            'discharged_total': 'INT',
            'recovery_rate': 'FLOAT',
            'cases_new': 'INT',
            'deaths_new': 'INT',
            'cfr': 'FLOAT',
            'tests_cumulative': 'INT',
            'tests_positive_cumulative': 'INT',
            'current_home_quarantine': 'INT',
            'current_institutional_quarantine': 'INT',
            'active_cases': 'INT'
        }
        return cols
