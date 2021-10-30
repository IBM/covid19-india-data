import sqlite3
from .db import DB


class CriticalCaseInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'HR_critical_case_info'
        self.table_desc = 'Haryana critical cases (patients on O2 support / ventilator) information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL',
            'facility_name': 'STRING NOT NULL',
            'patients_on_oxygen_support': 'INT',
            'patients_ventilator': 'INT',
            'total_patients': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, facility_name))"
        return query