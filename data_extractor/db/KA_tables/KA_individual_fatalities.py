import sqlite3
from .db import DB


class FatalitiesTable(DB):

    def __init__(self):
        self.table_name = 'KA_individual_fatalities'
        self.table_desc = 'Karnataka individual fatality diagnosis'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'patient_no': 'STRING NOT NULL PRIMARY KEY',
            'district_name': 'STRING',
            'age': 'INT',
            'sex': 'STRING',
            'description': 'STRING',
            'symptoms': 'STRING',
            'comorbidities': 'STRING',
            'doa': 'DATE',
            'dod': 'DATE',
            'place_of_death': 'STRING'
        }
        return cols
