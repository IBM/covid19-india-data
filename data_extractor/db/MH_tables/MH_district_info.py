import sqlite3
from .db import DB


class DistrictInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MH_district_caseinfo'
        self.table_desc = 'Maharashtra daily district level case information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL',
            'district_name': 'STRING NOT NULL',
            'cases_total': 'INT',
            'recoveries_total': 'INT',
            'deaths_total': 'INT',
            'deaths_total_other_causes': 'INT',
            'active_cases': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district_name))"
        return query