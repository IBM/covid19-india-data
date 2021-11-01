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
            'district': 'STRING NOT NULL',
            'sessions_24h': 'INT',
            'sessions_total': 'INT',
            'citizen_24h': 'INT',
            'citizen_60_plus_24h': 'INT',
            'citizen_60_plus_first_dose_total': 'INT',
            'citizen_45_to_59_24h': 'INT',
            'citizen_45_to_59_first_dose_total': 'INT',
            'citizen_45_plus_first_dose_total': 'INT',
            'citizen_45_plus_second_dose_total': 'INT',
            'citizen_18_to_44_first_dose_total': 'INT',
            'citizen_18_to_44_second_dose_total': 'INT',
            'health_care_worker_24h': 'INT',
            'health_care_worker_first_dose_total': 'INT',
            'health_care_worker_second_dose_total': 'INT',
            'front_line_worker_24h': 'INT',
            'front_line_worker_first_dose_total': 'INT',
            'front_line_worker_second_dose_total': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query