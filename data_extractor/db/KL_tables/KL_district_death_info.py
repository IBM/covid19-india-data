import sqlite3
from .db import DB


class DistrictDeathInfo(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_district_death_info'
        self.table_desc = 'District wise Death Cases through online and offline mode - post scrutiny status'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'deaths_reported': 'INT',
            'death_through_appeal': 'INT',
            'pending_deaths': 'INT',
            'death_cases_approved': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query

