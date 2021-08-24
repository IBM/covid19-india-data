import sqlite3
from .db import DB


class BulletinLinks(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'Metadata_Bulletin_Links'
        self.table_desc = 'Links to health bulletins for all states'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'state': 'STRING NOT NULL',
            'bulletin_link': 'STRING'
        }
        return cols

    def create_table(self):
        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, state))"
        return query
