import sqlite3
from .db import DB


class HospitalizationsTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_hospitalizations'
        self.table_desc = 'Delhi state asymptomatic, moderate, and severe patient numbers'
        self.cols = self.getcolumns()


    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'patients_in_hospital': 'INT',
            'asymptomatic_patients': 'INT',
            'moderate_patients': 'INT',
            'severe_patients': 'INT'
        }
        return cols
