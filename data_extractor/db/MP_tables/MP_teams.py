import sqlite3
from .db import DB


class Teams(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_teams'
        self.table_desc = 'Community, block, and district level teams formed to investigate patients on the basis of symptoms.'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'rrt': 'INT',
            'srrt': 'INT',
            'mmu': 'INT',
            'phmu': 'INT',
            'surveillance': 'INT',
        }
        return cols

