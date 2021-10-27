import sqlite3
from .db import DB


class DailyTestingInformation(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_testing_info'
        self.table_desc = 'Telangana daily testing information'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'tests_today': 'INT',
            'tests_cumulative': 'INT',
            'tests_per_million': 'INT',
            'reports_awaited': 'INT'
        }
        return cols
