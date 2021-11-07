import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        self.table_name = 'PB_cases'
        self.table_desc = 'Punjab samples, cases, and vaccination information. Table page 1'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'icu_patients_today': 'INT',
            'icu_patients_today_districts': 'STRING',
            'ventilator_patients_today': 'INT',
            'ventilator_patients_today_districts': 'STRING',
            'discharged_patients_today': 'INT',
            'discharged_patients_today_districts': 'STRING',
            'deaths_today': 'INT',
            'deaths_today_districts': 'STRING'
        }
        return cols
