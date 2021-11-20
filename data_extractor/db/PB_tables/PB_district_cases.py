import sqlite3
from .db import DB


class DistrictDetailsTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'PB_district_cases'
        self.table_desc = 'Daily and total district wise info. Multiple tables starting on page 2 and continuing page 4 or 5.'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'cases_today': 'INT',
            'percentage_tests_positive': 'FLOAT',
            'outside_source_details': 'STRING',
            'case_details': 'STRING',
            'remarks': 'STRING',
            'cases_total': 'INT',
            'active_cases': 'INT',
            'recovered_total': 'INT',
            'deaths_total': 'INT'
        }
        return cols

    def create_table(self):
        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
