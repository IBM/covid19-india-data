import sqlite3
from .db import DB


class ContactTravelNew(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_contact_travel_new'
        self.table_desc = 'Details of COVID-19 positive deaths in the last 24 hours'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'total_cases': 'INT',
            'history_of_travel': 'INT',
            'history_of_contact': 'INT',
            'no_history': 'INT'
        }
        return cols
