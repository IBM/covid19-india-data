import sqlite3
from .db import DB


class OutStateTable(DB):

    def __init__(self):
        self.table_name = 'PB_mucormycosis_out_of_state_details'
        self.table_desc = 'Punjab mucormycosis details of patients from out of state. Table on the last page of bulletins from June 2021'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'city': "STRING NOT NULL",
            'patients': 'INT',
            'deaths': 'INT'
        }
        return cols

    def create_table(self):
        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, city))"
        return query
