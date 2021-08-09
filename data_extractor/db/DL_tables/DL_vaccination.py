import sqlite3
from .db import DB


class VaccinationTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_vaccination'
        self.table_desc = 'Delhi state vaccination status'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'vax_total_24h': 'INT',
            'vax_first_dose_24h': 'INT',
            'vax_sec_dose_24h': 'INT',
            'vax_cumulative': 'INT',
            'vax_cumulative_first_dose': 'INT',
            'vax_cumulative_sec_dose': 'INT'
        }
        return cols
