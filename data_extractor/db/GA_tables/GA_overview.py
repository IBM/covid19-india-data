import sqlite3
from .db import DB


class Overview(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'GA_overview'
        self.table_desc = 'CASE INFO'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'recovery_rate': 'INT',
            'recovered_patients': 'INT',
            'recovery_in_last_24_hrs': 'INT',
            'home_isolation_cumulative': 'INT',
            'home_isolation_new': 'INT',
            'hospitalized_patients_cumulative': 'INT',
            'hospitalized_patients_new': 'INT',
            'samples_tested_cumulative': 'INT',
            'samples_tested_new': 'INT',
            'tests_per_million': 'INT',
            'total_cases_cunulative': 'INT',
            'total_cases_new': 'INT',
            'deaths_cumulative': 'INT',
            'deaths_new': 'INT',
            'active_cases': 'INT',
            'hospital_discharged': 'INT',
        }
        return cols
