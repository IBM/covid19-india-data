import sqlite3

from .db import Database
from .WB_tables import WB_case_info, WB_hospital, WB_testing, WB_district_cases, WB_testing_labs, \
    WB_PPE, WB_vaccination, WB_counselling

class WestBengalDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'case-info': WB_case_info.CaseInfoTable(),
            'testing': WB_testing.TestingTable(),
            'hospital': WB_hospital.HospitalInfraTable(),
            'district-cases': WB_district_cases.DistrictCasesTable(),
            'testing-labs': WB_testing_labs.TestingLabTable(),
            'ppe-info': WB_PPE.PPEUnitTable(),
            'vax-info': WB_vaccination.VaxInfoTable(),
            'counselling-info': WB_counselling.CounsellingInfoTable()
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
        