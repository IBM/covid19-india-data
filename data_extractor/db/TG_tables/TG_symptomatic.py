import sqlite3
from .db import DB


class SymptomaticCases(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_symptomatic'
        self.table_desc = 'Telangana status of asymptomatic / symptomatic cases'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'total_positives': 'INT',
            'total_asymptomatic': 'INT',
            'perc_asymptomatic': 'FLOAT',
            'total_symptomatic': 'INT',
            'perc_symptomatic': 'FLOAT'
        }
        return cols
