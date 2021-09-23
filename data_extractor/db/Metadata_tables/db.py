import sqlite3


class DB(object):

    def __init__(self):
        self.table_name = None
        self.table_desc = None
        self.cols = None

    def create_table(self):

        colstr = [f'`{colname}` {coltype}' for colname, coltype in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr})"
        return query

    def insert_row(self, cursor, **kwargs):

        cols = list(self.cols.keys())
        vals = [kwargs.get(col, None) for col in cols]
        colstr = ', '.join(cols)
        valstr = ', '.join(['?'] * len(cols))

        query = f'INSERT OR IGNORE INTO `{self.table_name}` ({colstr}) VALUES ({valstr})'
        cursor.execute(query, vals)
