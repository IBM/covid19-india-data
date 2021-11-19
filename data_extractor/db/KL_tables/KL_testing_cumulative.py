import sqlite3
from .db import DB


class TestingCumulative(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_cumulative_tests'
        self.table_desc = 'Cumulative number of samples tested'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'samples_sent': 'INT',
            'routine_sentinel_samples_pcr': 'INT',
            'airport_surveillance': 'INT',
            'CB_NAAT': 'INT',
            'True_NAT': 'INT',
            'POCT_PCR': 'INT',
            'RT_LAMP': 'INT',
            'Antigen_Assay': 'INT'
        }
        return cols
