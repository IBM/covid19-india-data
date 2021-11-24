import sqlite3
from .db import DB


class SurveillanceInfo(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_surveillance_info'
        self.table_desc = 'District wise distribution of persons under surveillance (quarantine and isolation)'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'cumulative_under_observation': 'INT',
            'cumulative_under_home_isolation': 'INT',
            'cumulative_hospitalized': 'INT',
            'new_hospitalized': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query

