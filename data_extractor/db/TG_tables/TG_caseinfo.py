import sqlite3
from .db import DB


class CaseInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_case_info'
        self.table_desc = 'Telangana daily new cases, recoveries, deaths information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'cases_new': 'INT',
            'cases_total': 'INT',
            'recovered_new': 'INT',
            'recovered_total': 'INT',
            'deaths_new': 'INT',
            'deaths_total': 'INT',
            'cases_in_isolation': 'INT',
            'state_CFR': 'FLOAT',
            'national_CFR': 'FLOAT',
            'state_recovery_rate': 'FLOAT',
            'national_recovery_rate': 'FLOAT'
        }
        return cols
