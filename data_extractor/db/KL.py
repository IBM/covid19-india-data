import sqlite3

from .db import Database
from .KL_tables import (
        KL_contact_travel_cumulative,
        KL_contact_travel_new,
        KL_critical_patients,
        KL_cumulative_summary_t_minus_one,
        KL_cumulative_summary,
        KL_daily_summary,
        KL_district_abstract,
        KL_district_case_info,
        KL_district_death_info,
        KL_individual_death_info,
        KL_psychosocial_support,
        KL_surveillance_info,
        KL_surveillance_info,
        KL_testing_cumulative,
        KL_testing_new,
        KL_travel_surveillance,
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
            'contact-travel-cumulative': KL_contact_travel_cumulative.ContactTravelCumulative(),
            'contact-travel-new': KL_contact_travel_new.ContactTravelNew(),
            'critical-patients': KL_critical_patients.CriticalPatients(),
            'cumulative-summary-t-minus-one': KL_cumulative_summary_t_minus_one.TMinusOneCumulativeSummary(),
            'cumulative-summary': KL_cumulative_summary.CumulativeSummary(),
            'daily-summary': KL_daily_summary.DailySummary(),
            'district-abstract': KL_district_abstract.DistrictAbstract(),
            'district-case-info': KL_district_case_info.DistrictCaseInfo(),
            'district-death-info': KL_district_death_info.DistrictDeathInfo(),
            'individual-death-info': KL_individual_death_info.IndividualDeathInfo(),
            'psychosocial-support': KL_psychosocial_support.PsychosocialSupport(),
            'surveillance-info': KL_surveillance_info.SurveillanceInfo(),
            'testing-cumulative': KL_testing_cumulative.TestingCumulative(),
            'testing-new': KL_testing_new.TestingNew(),
            'travel-surveillance': KL_travel_surveillance.TravelSurveillance(),
        }
        