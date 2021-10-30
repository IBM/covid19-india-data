import sqlite3
from .db import DB


class DailySummary(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_daily_summary'
        self.table_desc = 'Summary of new COVID-19 cases (last 24 hours)'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'positive_cases': 'INT',
            'active_cases': 'INT',
            'recovered': 'INT',
            'new_persons_in_surveillance': 'INT',
            'new_persons_in_home_ins_isolation': 'INT',
            'new_persons_in_hospital_isolation': 'INT',
            'daily_deaths': 'INT',
            'deaths_declared_as_per_appeal': 'INT',
            'pending_deaths': 'INT'
        }
        return cols
