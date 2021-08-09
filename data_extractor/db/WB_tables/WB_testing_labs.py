import sqlite3
from .db import DB


class TestingLabTable(DB):

    def __init__(self):
        self.table_name = 'WB_testing_labs'
        self.table_desc = 'West Bengal testing laboratories information'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'testing_lab_name': 'STRING',
            'district': 'STRING',
            'authority': 'STRING',
            'samples_tested': 'INT',
            'testing_method': 'STRING',
            'functional_wef': 'STRING'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, testing_lab_name))"
        return query