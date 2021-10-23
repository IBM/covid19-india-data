import sqlite3
from .db import DB


class DistrictCaseInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_district_cases_info'
        self.table_desc = 'Telangana daily new cases in districts'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'district': 'STRING NOT NULL',
            'cases_new': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query