import sqlite3
from .db import DB


class DistrictCasesTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KA_district_cases'
        self.table_desc = 'Karnataka districtwise abstract'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'cases_new': 'INT',
            'cases_total': 'INT',
            'discharged_new': 'INT',
            'discharged_total': 'INT',
            'active_cases_total': 'INT',
            'deaths_new': 'INT',
            'deaths_total': 'INT',
            'non_covid_deaths': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
