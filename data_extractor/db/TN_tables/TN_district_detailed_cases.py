import sqlite3
from .db import DB

class DistrictDetailsTable(DB):
    def __init__(self):
        self.table_name = "TN_district_details"
        self.table_desc = "Tamil Nadu district wise details, table on pages 3, 4 and 6"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'total_active_cases_till_yesterday': 'INT',
            'new_cases_today': 'INT',
            'discharged_cases_today': 'INT',
            'deaths_today': 'INT',
            'total_active_cases_including_today': 'INT',
            'total_indegenous_cases_till_yesterday': 'INT',
            'indegenous_cases_today': 'INT',
            'total_imported_cases_till_yesterday': 'INT',
            'imported_cases_today': 'INT',
            'total_cases_till_today': 'INT',
            'total_cases_discharged': 'INT',
            'total_deaths': 'INT'
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
