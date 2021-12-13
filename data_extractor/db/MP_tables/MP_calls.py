import sqlite3
from .db import DB


class Calls(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_calls'
        self.table_desc = 'Toll free helplines of COVID.'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'information': 'INT',
            'medical_advice': 'INT',
            'counselling': 'INT',
            'complaint': 'INT',
            'total': 'INT',
        }
        return cols

