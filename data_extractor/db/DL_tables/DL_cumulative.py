import sqlite3
from .db import DB


class CumulativeTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_cumulative'
        self.table_desc = 'Delhi state cumulative positive, recovered, fatalities data'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'cumulative_positive_cases': 'INT',
            'cumulative_positivity_rate': 'FLOAT',
            'cumulative_recovered': 'INT',
            'cumulative_deaths': 'INT',
            'cumulative_cfr': 'FLOAT',
            'active_cases': 'INT'
        }
        return cols
