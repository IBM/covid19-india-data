import sqlite3
from .db import DB


class CounsellingInfoTable(DB):

    def __init__(self):
        self.table_name = 'WB_counselling'
        self.table_desc = 'West Bengal ambulance and tele-counselling information'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'general_queries_24h': 'INT',
            'general_queries_cum': 'INT',
            'consultations_24h': 'INT',
            'consultations_total': 'INT',
            'ambulances_assigned_24h': 'INT',
            'ambulance_calls_24h': 'INT',
            'telepsych_counselling_24h': 'INT',
            'telepsych_counselling_total': 'INT'
        }
        return cols
