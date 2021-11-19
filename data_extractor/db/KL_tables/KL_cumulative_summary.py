import sqlite3
from .db import DB


class CumulativeSummary(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_cumulative_summary'
        self.table_desc = 'Cumulative summary'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'total_positive_cases': 'INT',
            'active_cases': 'INT',
            'total_recovered': 'INT',
            'total_persons_in_surveillance': 'INT',
            'total_persons_in_home_ins_isolation': 'INT',
            'total_persons_in_hospital_isolation': 'INT',
            'total_deaths': 'INT',
            'total_deaths_declared_as_per_appeal': 'INT',
            'total_pending_deaths': 'INT'
        }
        return cols
