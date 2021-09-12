import sqlite3
from .db import DB

class AirportSurveillanceTable(DB):
    def __init__(self):
        self.table_name = "TN_airport_surveillance"
        self.table_desc = "Tamil Nadu 4 airports domestic flights passenger testing details till previous day, table number 2 from the top on third last page"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'airport': 'STRING',
            'flights_arrived': 'INT',
            'passengers': 'INT',
            'positive_cases': 'INT'
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, airport))"
        return query
