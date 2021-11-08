import sqlite3
from .db import DB


class DistrictTestingTable(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'UK_testing'
        self.table_desc = 'Uttarakhand district wise testing snapshot'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district_name': 'STRING NOT NULL',
            'samples_collected_today': 'INT',
            'samples_collected_cumulative': 'INT',
            'negative_results_today': 'INT',
            'negative_results_total': 'INT',
            'positive_results_today': 'INT',
            'positive_results_total': 'INT',
            'samples_results_awaited': 'INT',
            'rejected_samples': 'INT'
        }
        return cols

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district_name))"
        return query