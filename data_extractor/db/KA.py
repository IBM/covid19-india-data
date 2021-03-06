import sqlite3

from .db import Database
from .KA_tables import KA_case_info, KA_district_cases, KA_individual_fatalities

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
            'individual-fatalities': KA_individual_fatalities.FatalitiesTable()
        }
        