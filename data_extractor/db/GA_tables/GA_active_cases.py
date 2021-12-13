import sqlite3
from .db import DB


class ActiveCases(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'GA_active_cases'
        self.table_desc = 'BREAKUP OF ACTIVE POSITIVE CASES'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING',
            'location': 'STRING NOT NULL',
            'cases': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, location))"
        return query