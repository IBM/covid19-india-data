import sqlite3
from .db import DB


class ComorbiditiesFatalityCount(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_comorbidities_fatalities'
        self.table_desc = 'Telangana percentage of deaths due to COVID-19 or comorbidities'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'perc_fatality_covid19': 'FLOAT',
            'perc_fatality_comorbities': 'FLOAT'
        }
        return cols
