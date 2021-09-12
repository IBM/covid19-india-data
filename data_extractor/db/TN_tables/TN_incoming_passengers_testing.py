import sqlite3
from .db import DB

class IncomingPassengersTable(DB):
    def __init__(self):
        self.table_name = "TN_incoming_people_till_yesterday"
        self.table_desc = "Tamil Nadu incoming people from various mode of transport, first table from the top on third last page of bulletin"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'mode_of_travel': 'STRING',
            'total_passengers': 'INT',
            'total_positive_cases': 'INT',
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, mode_of_travel))"
        return query
