import sqlite3
from .db import DB


class DistrictAbstract(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_district_abstract'
        self.table_desc = 'District wise abstract of number of LSGs and Wards with WISP > 10'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'LSG': 'INT',
            'Wards': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query

