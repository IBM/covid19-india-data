import sqlite3

from .db import Database
from .UK_tables import UK_district_wise_cases, UK_district_wise_mucormycosis_cases, \
    UK_district_wise_testing, UK_district_wise_vaccination, UK_hospital_wise_deaths


class UttarakhandDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'district-cases': UK_district_wise_cases.DistrictCasesTable(),
            'district-mucormycosis-cases': UK_district_wise_mucormycosis_cases.DistrictMucormycosisCasesTable(),
            'district-testing': UK_district_wise_testing.DistrictTestingTable(),
            'district-vaccination': UK_district_wise_vaccination.DistrictVaccinationTable(),
            'hospital-deaths': UK_hospital_wise_deaths.HospitalDeathsTable()
        }

    def insert_row(self, data):

        cursor = self.conn.cursor()

        # Insert data in all the relevant tables
        for id, tableobj in self.tables.items():
            if id not in data:
                continue

            vals = data[id]

            if isinstance(vals, dict):
                tableobj.insert_row(cursor=cursor, **vals)
            elif isinstance(vals, list):
                for valitem in vals:
                    tableobj.insert_row(cursor=cursor, **valitem)

        self.conn.commit()
