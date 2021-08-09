import sqlite3
from .db import DB


class HospitalInfraTable(DB):

    def __init__(self):
        self.table_name = 'WB_hospital'
        self.table_desc = 'West Bengal hospital infrastructure snapshot'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'hospital_dedicated': 'INT',
            'hospital_dedicated_govt': 'INT',
            'hospital_dedicated_pvt': 'INT',
            'covid19_beds': 'INT',
            'covid19_bed_occupancy': 'FLOAT',
            'icu_hdu_beds': 'INT',
            'n_safe_homes': 'INT',
            'safe_home_beds': 'INT',
            'n_ventilators': 'INT',
            'total_patients_home_isolation': 'INT',
            'current_patients_home_isolation': 'INT',
            'released_patients_home_isolation': 'INT',
            'current_patients_hospital': 'INT',
            'current_patients_safe_homes': 'INT'
        }
        return cols
