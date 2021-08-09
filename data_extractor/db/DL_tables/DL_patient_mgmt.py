import sqlite3
from .db import DB


class PatientMgmtTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_patient_mgmt'
        self.table_desc = 'Patient management table containing hospital occupany information for Delhi'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'hospital_beds_total': 'INT',
            'hospital_beds_occupied': 'INT',
            'hospital_beds_vacant': 'INT',
            'covid_care_center_beds_total': 'INT',
            'covid_care_center_beds_occupied': 'INT',
            'covid_care_center_beds_vacant': 'INT',
            'covid_health_center_beds_total': 'INT',
            'covid_health_center_beds_occupied': 'INT',
            'covid_health_center_beds_vacant': 'INT',
            'home_isolation_count': 'INT'
        }
        return cols
