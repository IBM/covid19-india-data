import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_case_info'
        self.table_desc = 'Delhi state case, recovered, and death information'
        self.cols = self.getcolumns()


    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'cases_positive': 'INT',
            'tests_conducted': 'INT',
            'positivity_rate': 'FLOAT',
            'cases_recovered': 'INT',
            'deaths': 'INT'
        }
        return cols
