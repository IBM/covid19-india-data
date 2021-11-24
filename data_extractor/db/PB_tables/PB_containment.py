import sqlite3
from .db import DB


class ContainmentZonesTable(DB):

    def __init__(self):
        self.table_name = 'PB_containment_zone'
        self.table_desc = 'Details about larger containment zones, with population contained in each. Table starting from Page 4 or 5 and can extend over multiple pages'
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
