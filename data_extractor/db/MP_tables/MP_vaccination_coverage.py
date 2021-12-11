import sqlite3
from .db import DB


class VaccinationCoverage(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'MP_vaccination_coverage'
        self.table_desc = 'Vaccination Coverage'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'doses_today': 'INT',
            'doses_total': 'INT',
        }
        return cols


    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query