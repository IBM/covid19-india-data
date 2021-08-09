import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        self.table_name = 'WB_case_info'
        self.table_desc = 'West Bengal case, discharge, and fatality information'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'cases_new': 'INT',
            'cases_total': 'INT',
            'discharged_total': 'INT',
            'discharged_new': 'INT',
            'deaths_total': 'INT',
            'deaths_new': 'INT',
            'cases_active_total': 'INT',
            'cases_active_new': 'INT',
            'discharge_rate': 'FLOAT',
            'fatality_rate': 'FLOAT'
        }
        return cols
