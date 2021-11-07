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
            'cases_today': 'INT',
            'percentage_tests_positive': 'FLOAT',
            'case_details': 'STRING',
            'remarks': 'STRING',
            'cases_total': 'INT',
            'active_cases_total': 'INT',
            'total_cured': 'INT',
            'deaths_total': 'INT'
        }
        return cols

    def create_table(self):
        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
