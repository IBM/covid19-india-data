import sqlite3
from .db import DB


class BedCapacity(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'GA_bed_capacity'
        self.table_desc = 'BED CAPACITY IN COVID CARE CENTRES'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'total_capacity': 'INT',
            'vacant_capacity': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query