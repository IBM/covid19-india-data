import sqlite3
from .db import DB


class VaxInfoTable(DB):

    def __init__(self):
        self.table_name = 'WB_vaccination'
        self.table_desc = 'West Bengal vaccination information'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'total_vax_today': 'INT',
            'first_dose_today': 'INT',
            'second_dose_today': 'INT',
            'cumulative_vax': 'INT',
            'cumulative_vax_first_dose': 'INT',
            'cumulative_vax_sec_dose': 'INT',
            'cvc_count': 'INT',
            'aefi_cases': 'INT',
            'vax_wastage': 'FLOAT'
        }
        return cols
