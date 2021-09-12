import sqlite3
from .db import DB

class SeaportSurveillanceTable(DB):
    def __init__(self):
        self.table_name = "TN_seaport_surveillance"
        self.table_desc = "Tamil Nadu seaport surveillance till the day before, table number 2 from the top on last page"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'seaport': 'STRING',
            'ships_arrived': 'INT',
            'passengers': 'INT',
            'positive_cases': 'INT'
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, seaport))"
        return query
