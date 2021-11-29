import sqlite3
from .db import DB


class IndividualDeathInfo(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_individual_death_info'
        self.table_desc = 'Details of COVID-19 positive deaths in the last 24 hours'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'name': 'STRING',
            'district': 'STRING',
            'place': 'STRING',
            'age': 'INT',
            'gender': 'STRING',
            'death_date': 'DATE'
        }
        return cols
