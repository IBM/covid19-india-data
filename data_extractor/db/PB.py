import sqlite3

from .db import Database
from .PB_tables import PB_case_details, PB_cases_samples_vaccination, PB_district_cases, PB_containment,\
    PB_micro_containment, PB_mucormycosis_details, PB_mucormycosis_district_details, PB_mucormycosis_out_state_details

class PunjabDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'cases-samples-vaccination': PB_cases_samples_vaccination.CaseDetailsTable(),
            'cases': PB_case_details.CaseInfoTable(),
            'district': PB_district_cases.DistrictDetailsTable(),
            'containment': PB_containment.ContainmentZonesTable(),
            'micro-containment': PB_micro_containment.ContainmentInfoTable(),
            'muco-details': PB_mucormycosis_details.CaseInfoTable(),
            'muco-district-info': PB_mucormycosis_district_details.DistrictInfoTable(),
            'out-state-info': PB_mucormycosis_out_state_details.OutStateTable()
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
        
