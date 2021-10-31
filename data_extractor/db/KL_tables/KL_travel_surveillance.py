import sqlite3
from .db import DB


class TravelSurveillance(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_travel_surveillance'
        self.table_desc = 'Summary of Travel Surveillance'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'international_cumulative': 'INT',
            'domestic_cumulative': 'INT',
            'total': 'INT'
        }
        return cols

