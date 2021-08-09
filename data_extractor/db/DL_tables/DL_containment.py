import sqlite3
from .db import DB


class ContainmentTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'DL_containment'
        self.table_desc = 'Delhi state containment zones'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'containment_zones': 'INT',
            'calls_covid_helpline': 'INT',
            'calls_ambulance_total': 'INT',
            'calls_refused': 'INT'
        }
        return cols
