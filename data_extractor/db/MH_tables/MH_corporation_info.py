import sqlite3
from .db import DB


class CorporationInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MH_corporation_caseinfo'
        self.table_desc = 'Maharashtra daily municipal corporation level case information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL',
            'district_name': 'STRING NOT NULL',
            'cases_daily': 'INT',
            'cases_total': 'INT',
            'deaths_daily': 'INT',
            'deaths_total': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district_name))"
        return query