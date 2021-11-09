import sqlite3
from .db import DB


class CaseInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'HR_case_info'
        self.table_desc = 'Haryana daily new cases, recoveries, deaths information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'samples_taken_today': 'INT',
            'samples_sent_cumulative': 'INT',
            'samples_negative_cumulative': 'INT',
            'samples_positive_cumulative_total': 'INT',
            'samples_positive_cumulative_male': 'INT',
            'samples_positive_cumulative_female': 'INT',
            'samples_positive_cumulative_transgender': 'INT',
            'samples_results_awaited': 'INT',
            'cases_new': 'INT',
            'people_put_on_surveillance_cumulative': 'INT',
            'people_completed_surveillance_cumulative': 'INT',
            'people_currently_under_surveillance': 'INT',
            'people_home_isolation': 'INT',
            'recoveries_cumulative': 'INT',
            'active_cases': 'INT',
            'deaths_total': 'INT',
            'deaths_male': 'INT',
            'deaths_female': 'INT',
            'deaths_transgender': 'INT',
            'vax_today_total': 'INT',
            'vax_today_first_dose': 'INT',
            'vax_today_second_dose': 'INT',
            'vax_cumulative': 'INT',
            'positivity_rate_today': 'FLOAT',
            'positivity_rate_cumulative': 'FLOAT',
            'recovery_rate': 'FLOAT',
            'fatality_rate': 'FLOAT',
            'tests_per_million': 'INT'
        }
        return cols
