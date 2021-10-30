import sqlite3

from .db import Database
from .KA_tables import KA_case_info, KA_district_cases

class KarnatakaDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'case-info': KA_case_info.CaseInfoTable(),
            'district-cases': KA_district_cases.DistrictCasesTable(),
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
        