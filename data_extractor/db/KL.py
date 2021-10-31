import sqlite3

from .db import Database
from .KL_tables import (
        KL_cumulative_summary_t_minus_one,
        KL_daily_summary,
        KL_cumulative_summary,
        KL_district_case_info,
        KL_district_death_info,
        KL_contact_travel_cumulative,
        KL_contact_travel_new,
        KL_individual_death_info,
        KL_critical_patients,
        KL_cumulative_tests,
        KL_new_tests,
        KL_surveillance_info,
        KL_travel_surveillance,
        KL_psychosocial_support,
        KL_surveillance_info,
    )

class KeralaDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'cumulative-summary-t-minus-one': KL_cumulative_summary_t_minus_one.TMinusOneCumulativeSummary(),
            'daily-summary': KL_daily_summary.DailySummary(),
            'cumulative-summary': KL_cumulative_summary.CumulativeSummary(),
            'district-case-info': KL_district_case_info.DistrictCaseInfo(),
            'district-death-info': KL_district_death_info.DistrictDeathInfo(),
            'contact-travel-cumulative': KL_contact_travel_cumulative.ContactTravelCumulative(),
            'contact-travel-new': KL_contact_travel_new.ContactTravelNew(),
            'individual-death-info': KL_individual_death_info.IndividualDeathInfo(),
            'critical-patients': KL_critical_patients.CriticalPatients(),
            'testing-cumulative': KL_cumulative_tests.TestingCumulative(),
            'testing-new': KL_new_tests.TestingNew(),
            'surveillance-info': KL_surveillance_info.SurveillanceInfo(),
            'travel-surveillance': KL_travel_surveillance.TravelSurveillance(),
            'psychosocial-support': KL_psychosocial_support.PsychosocialSupport(),
            'district-abstract': KL_district_abstract.DistrictAbstract(),
        }
        