import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'UK_case_info'
        self.table_desc = 'Uttarakhand daily and cumulative state-level case information'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'cases_new': 'INT',
            'tests_today': 'INT',
            'tests_total': 'INT',
            'cases_total': 'INT',
            'discharged_total': 'INT',
            'deaths_total': 'INT',
            'active_cases': 'INT',
            'vax_today': 'INT'
        }
        return cols
