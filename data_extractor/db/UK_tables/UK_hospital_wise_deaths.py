import sqlite3
from .db import DB


class HospitalDeathsTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'UK_hopital_wise_deaths'
        self.table_desc = 'Uttarakhand hospital wise deaths info'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'hospital_name': 'STRING NOT NULL',
            'deaths_new': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, hospital_name))"
        return query
