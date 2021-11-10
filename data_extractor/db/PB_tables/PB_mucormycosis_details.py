import sqlite3
from .db import DB


class CaseInfoTable(DB):

    def __init__(self):
        self.table_name = 'PB_mucormycosis_cases'
        self.table_desc = 'Punjab mucormycosis cases daily and total information. Table on the second last page of bulletins since June 2021.'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'new_cases': 'INT',
            'deaths_today': 'INT',
            'cured_today': 'INT',
            'cases_total': 'INT',
            'cases_belonging_punjab': 'INT',
            'cases_belonging_other_states': 'INT',
            'under_treatment_total': 'INT',
            'under_treatment_belonging_punjab': 'INT',
            'under_treatment_beloging_other_states': 'INT',
            'cured_total': 'INT',
            'cured_total_belonging_punjab': 'INT',
            'cured_total_belonging_other_states': 'INT',
            'deaths_total': 'INT',
            'deaths_total_belonging_punjab': 'INT',
            'deaths_total_belonging_other_states': 'INT',
            'lama': 'INT',
            'lama_belonging_punjab': 'INT',
            'lama_belonging_other_states': 'INT'
        }
        return cols
