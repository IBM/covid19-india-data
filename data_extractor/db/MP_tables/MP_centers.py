import sqlite3
from .db import DB


class Centers(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_centers'
        self.table_desc = 'Government and private institutions have been identified \
                           as Dedicated COVID Care Center (DCCC), Dedicated COVID \
                           Health Center (DCHC), and Dedicated Covid Hospital (DCH) \
                           by the government for the treatment of corona positive \
                           persons, in which the treatment of corona infected persons \
                           is being done on the basis of symptoms and severity.'

        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'category': 'STRING NOT NULL',
            'number_of': 'INT',
            'total_isolation_beds': 'INT',
            'total_icu_beds': 'INT',
            'total_beds': 'INT',
            'total_ventilators': 'INT',
        }
        return cols


    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, category))"
        return query