import sqlite3
from .db import DB


class CaseDetailsTable(DB):

    def __init__(self):
        self.table_name = 'PB_cases'
        self.table_desc = 'Punjab samples, cases, and vaccination information. Table page 1'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'samples_total': 'INT',
            'samples_new': 'INT',
            'tests_new': 'INT',
            'cases_total': 'INT',
            'discharged_total': 'INT',
            'active_cases': 'INT',
            'deaths_total': 'INT',
            'oxygen_support_active_patients': 'INT',
            'critical_care_active_patients': 'INT',
            'ventilator_support_active_patients': 'INT',
            'healthcare_first_vaccination_today': 'INT',
            'healthcare_first_vaccination_total': 'INT',
            'frontline_first_vaccination_today': 'INT',
            'frontline_first_vaccination_total': 'INT',
            'healthcare_second_vaccination_today': 'INT',
            'healthcare_second_vaccination_total': 'INT',
            'frontline_second_vaccination_today': 'INT',
            'frontline_second_vaccination_total': 'INT',
            'above_45_first_vaccination_today': 'INT',
            'above_45_first_vaccination_total': 'INT',
            'above_45_second_vaccination_today': 'INT',
            'above_45_second_vaccinattion_total': 'INT',
            'eighteen_44_first_vaccination_today': 'INT',
            'eighteen_44_first_vaccination_total': 'INT',
            'eighteen_44_second_vaccination_today': 'INT',
            'eighteen_44_second_vaccination_total': 'INT',
            'first_vaccination_today': 'INT',
            'second_vaccination_today': 'INT',
            'total_vaccination_today': 'INT'
        }
        return cols
