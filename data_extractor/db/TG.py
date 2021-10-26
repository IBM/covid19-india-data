import sqlite3

from .db import Database
from .TG_tables import TG_symptomatic, TG_comorbidities, TG_agedist, TG_caseinfo, \
    TG_testinfo, TG_contact_testing, TG_district_cases

class TelanganaDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'case-information': TG_caseinfo.CaseInformation(),
            'testing-information': TG_testinfo.DailyTestingInformation(),
            'contact-testing-info': TG_contact_testing.ContactTestingInformation(),
            'district-wise-info': TG_district_cases.DistrictCaseInformation(),
            'asymptomatic-status': TG_symptomatic.SymptomaticCases(),
            'agewise-info': TG_agedist.AgeGenderDist(),
        }
        