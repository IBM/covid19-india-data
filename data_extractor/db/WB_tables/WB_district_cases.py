import sqlite3
from .db import DB


class DistrictCasesTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'WB_district_cases'
        self.table_desc = 'West Bengal district wise case info'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'cases_total': 'INT',
            'cases_new': 'INT',
            'discharged_total': 'INT',
            'discharged_new': 'INT',
            'deaths_total': 'INT',
            'deaths_new': 'INT',
            'active_cases_new': 'INT',
            'active_cases_total': 'INT',
            'last_reported_case': 'DATE'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
