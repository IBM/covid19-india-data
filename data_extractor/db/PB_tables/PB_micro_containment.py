import sqlite3
from .db import DB


class ContainmentInfoTable(DB):

    def __init__(self):
        self.table_name = 'PB_micro_containment_zone'
        self.table_desc = 'Details about micro containment zones in a district, with population contained. Table starting on page 4 or 5 and can extend over multiple pages.'
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
