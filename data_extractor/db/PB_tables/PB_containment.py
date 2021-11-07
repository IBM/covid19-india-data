import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        self.table_name = 'PB_containment_zone'
        self.table_desc = 'Punjab containment and micro containment zones in district. Tables on page 5.'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'containment': 'STRING NOT NULL',
            'population_contained': 'INT'
        }
        return cols


    def create_table(self):
        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district, containment))"
        return query
