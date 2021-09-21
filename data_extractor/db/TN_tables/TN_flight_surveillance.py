import sqlite3
from .db import DB

class FlightSurveillanceTable(DB):
    def __init__(self):
        self.table_name = "TN_flight_details"
        self.table_desc = "Tamil Nadu 4 airports domestic flights passenger testing details till previous day, table number 3 from the top on third last page which continues to second last page"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'airport': 'STRING NOT NULL'
            'flight': 'STRING NOT NULL',
            'total_passengers': 'INT',
            'passengers_tested': 'INT',
            'tests_under_process': 'INT',
            'tests_negative': 'INT',
            'positive_during_entry_screening': 'INT',
            'positive_during_exit_screening': 'INT'
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, airport, flight))"
        return query
