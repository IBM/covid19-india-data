import sqlite3
from .db import DB

class DetailedInfoTable(DB):
    def __init__(self):
        self.table_name = "TN_positive_cases_detail"
        self.table_desc = "Tamil Nadu positive cases details by sex, table 1 on page 2 of bulletin"
        self.cols = self.getcolumns()

    def getcolumns(self):
        
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'active_cases': 'INT',
            'tested_positive_today': 'INT',
            'tested_positive_till_date': 'INT',
            'rtpcr_samples_tested_today': 'INT',
            'rtpcr_samples_tested_till_date': 'INT',
            'persons_tested_rt_pcr_today': 'INT',
            'persons_tested_rt_pcr_till_date': 'INT',
            'male_positive_tests_today': 'INT',
            'female_positive_tests_today': 'INT',
            'transgender_positive_tests_today': 'INT',
            'male_positive_tests_till_date': 'INT',
            'female_positive_tests_till_date': 'INT',
            'transgender_positive_tests_till_date': 'INT',
            'discharged_today': 'INT',
            'discharged_total': 'INT',
            'deaths_today': 'INT',
            'deaths_total': 'INT',
            'deaths_private_hospitals': 'INT',
            'deaths_government_hopitals': 'INT',
        }

        return cols
