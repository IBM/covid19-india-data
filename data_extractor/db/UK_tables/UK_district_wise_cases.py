import sqlite3
from .db import DB


class DistrictCasesTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'UK_district_cases'
        self.table_desc = 'Uttarakhand district wise case info'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'cases_total': 'INT',
            'recovered_total': 'INT',
            'active_cases': 'INT',
            'deaths_total': 'INT',
            'migrated_total': 'INT',
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
