import sqlite3
from .db import DB


class DistrictCaseInfo(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_district_case_info'
        self.table_desc = 'District wise summary of Cumulative cases, Active cases, and New positive cases'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'declared_positive': 'INT',
            'declared_negative': 'INT',
            'positive_cases_admitted': 'INT',
            'other_districts': 'STRING'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query

