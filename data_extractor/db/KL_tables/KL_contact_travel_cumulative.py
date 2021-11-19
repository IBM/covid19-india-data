import sqlite3
from .db import DB


class ContactTravelCumulative(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_contact_travel_cumulative'
        self.table_desc = 'Summary of contact or travel history of COVID-19 cases since 4th May 2020'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'total_cases': 'INT',
            'history_of_travel': 'INT',
            'history_of_contact': 'INT'
        }
        return cols
