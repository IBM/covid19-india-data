import sqlite3
from .db import DB

class DeathMorbiditiesTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TN_comorbidities_deaths'
        self.table_desc = 'Tamil Nadu comorbidities or non comorbidities death facilitiestype, two tables on page 10'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'comorbidities_government_dme': 'INT',
            'comorbidities_government_dms': 'INT',
            'comorbidities_private': 'INT',
            'comorbidities_other_government_institutions': 'INT',
            'no_comorbidities_government_dme': 'INT',
            'no_comorbidities_government_dms': 'INT',
            'no_comorbidities_private': 'INT',
            'no_comorbidities_other_government_institutions': 'INT',
        }

        return cols
