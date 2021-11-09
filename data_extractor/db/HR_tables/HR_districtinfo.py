import sqlite3
from .db import DB


class DistrictInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'HR_district_info'
        self.table_desc = 'Haryana district-wise case information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL',
            'district_name': 'STRING NOT NULL',
            'positive_cases_today': 'INT',
            'positive_cases_cumulative': 'INT',
            'recovered_total': 'INT',
            'recovered_new': 'INT',
            'recovery_rate': 'FLOAT',
            'deaths_with_comorbidity': 'INT',
            'deaths_without_comorbidity': 'INT',
            'deaths_total': 'INT',
            'deaths_new': 'INT',
            'active_cases_less_11days': 'INT',
            'active_cases_more_11days': 'INT',
            'active_cases_total': 'INT',
            'vaccination_dose1': 'INT',
            'vaccination_dose2': 'INT',
            'vaccination_total': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district_name))"
        return query