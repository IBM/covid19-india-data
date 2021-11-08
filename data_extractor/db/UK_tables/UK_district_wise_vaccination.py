import sqlite3
from .db import DB


class DistrictVaccinationTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'UK_vaccination'
        self.table_desc = 'Uttarakhand district wise vaccination snapshot'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district_name': 'STRING NOT NULL',
            'sessions_24h': 'INT',
            'sessions_total': 'INT',
            'citizen_24h': 'INT',
            'citizen_60_plus_24h': 'INT',
            'citizen_60_plus_dose1_total': 'INT',
            'citizen_45_to_59_24h': 'INT',
            'citizen_45_to_59_dose1_total': 'INT',
            'citizen_45_plus_dose1_total': 'INT',
            'citizen_45_plus_dose2_total': 'INT',
            'citizen_18_to_44_dose1_total': 'INT',
            'citizen_18_to_44_dose2_total': 'INT',
            'HCW_24h': 'INT',
            'HCW_dose1_total': 'INT',
            'HCW_dose2_total': 'INT',
            'FLW_24h': 'INT',
            'FLW_dose1_total': 'INT',
            'FLW_dose2_total': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district_name))"
        return query