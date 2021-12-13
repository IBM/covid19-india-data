import sqlite3
from .db import DB


class DistrictInfo(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_district_info'
        self.table_desc = 'District level information'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'new_positive': 'INT',
            'cumulative_positive': 'INT',
            'new_deaths': 'INT',
            'cumulative_deaths': 'INT',
            'new_recovered': 'INT',
            'cumulative_recovered': 'INT',
            'active_cases': 'INT'
        }
        return cols


    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query