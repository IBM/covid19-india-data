import sqlite3
from .db import DB

class IndividualFatalities(DB):
    def __init__(self):
        self.table_name = "TN_individual_fatalities"
        self.table_desc = "Tamil Nadu individual fatality diagnosis data"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'case_id': 'INT NOT NULL',
            'category': 'STRING',
            'age': 'INT',
            'gender': 'STRING',
            'location': 'STRING',
            'comorbidity': 'STRING',
            'test_date': 'STRING',
            'test_details': 'STRING',
            'admission_location': 'STRING',
            'admission_date': 'STRING',
            'admission_time': 'STRING',
            'admission_symptoms_days': 'INT',
            'admission_symptoms_details': 'STRING',
            'death_cause': 'STRING',
            'death_date': 'STRING',
            'death_time': 'STRING',
            'raw_data': 'STRING'
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, case_id))"
        return query
