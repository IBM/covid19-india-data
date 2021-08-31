import sqlite3
from .db import DB

class DetailedInfoTable(DB):
    def __init__(self):
        self.table_name = "TN_health_measures"
        self.table_desc = "Tamil Nadu cumulative info, table 1 on page 2 of bulletin"
        self.cols = self.getcolumns()

    def getcolumns(self):
        # total means value till date
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'total_active_cases': 'INT',
            'tested_positive_today': 'INT',
            'returned_road_positive_today': 'INT',
            'total_new_cases': 'INT',
            'total_tested_positive': 'INT',
            'rt_pcr_today': 'INT',
            'total_rt_pcr': 'INT',
            'persons_tested_rt_pcr': 'INT',
            'total_persons_tested_rt_pcr': 'INT',
            'male_positive_tests': 'INT',
            'female_positive_tests': 'INT',
            'transgender_positive_tests': 'INT',
            'total_male_positive_tests': 'INT',
            'total_female_positive_tests': 'INT',
            'total_transgender_positive_tests': 'INT',
            'testing_facilities': 'INT',
            'government_testing_facilities': 'INT',
            'private_testing_facilities': 'INT',
            'discharged_today': 'INT',
            'total_discharged': 'INT',
            'deaths_today': 'INT',
            'deaths_private_hospitals': 'INT',
            'deaths_government_hopitals': 'INT',
            'total_deaths': 'INT'
        }

        return cols
