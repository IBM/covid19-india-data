import sqlite3
from .db import DB


class DistrictMucormycosisCasesTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'UK_mucormycosis_cases'
        self.table_desc = 'Uttarakhand mucormycosis case info'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district_name': 'STRING NOT NULL',
            'hospital_name': 'STRING NOT NULL',
            'cases_new': 'INT',
            'deaths_new': 'INT',
            'discharged_new': 'INT',
            'cases_total': 'INT',
            'deaths_total': 'INT',
            'discharged_total': 'INT',
            'migrated_total': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district_name, hospital_name))"
        return query
