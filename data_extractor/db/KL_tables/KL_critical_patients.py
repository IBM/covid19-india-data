import sqlite3
from .db import DB


class CriticalPatients(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_critical_patients'
        self.table_desc = 'Summary of critical patients'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'patients_in_icu': 'INT',
            'patients_on_ventillation': 'INT'
        }
        return cols
