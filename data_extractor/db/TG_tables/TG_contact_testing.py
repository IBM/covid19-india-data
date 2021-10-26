import sqlite3
from .db import DB


class ContactTestingInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_contact_testing'
        self.table_desc = 'Telangana primary and secondary contact testing'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'tests_today': 'INT',
            'tests_cumulative': 'INT',
            'primary_contacts_tested_today': 'INT',
            'perc_primary_contacts_tested_today': 'FLOAT',
            'sec_contacts_tested_today': 'INT',
            'perc_sec_contacts_tested_today': 'FLOAT'
        }
        return cols
