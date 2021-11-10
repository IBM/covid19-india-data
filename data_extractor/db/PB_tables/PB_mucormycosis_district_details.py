import sqlite3
from .db import DB


class DistrictInfoTable(DB):

    def __init__(self):
        self.table_name = 'PB_mucormycosis_district_cases'
        self.table_desc = 'Punjab mucormycosis district wise details for total, deaths etc. Table on the last page of bulletins from June 2021'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': "STRING NOT NULL",
            'cases_today': 'INT',
            'deaths_today': 'INT',
            'cases_total': 'INT',
            'deaths_total': 'INT',
            'under_treatment': 'INT',
            'cured_total': 'INT',
            'patients_belonging_other_states': 'INT',
            'deaths_belonging_other_states': 'INT'
        }
        return cols

    def create_table(self):
        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY date, district))"
        return query
