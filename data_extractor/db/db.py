import os
import sqlite3


class Database(object):
    def __init__(self, datadir):
        self.datadir = datadir
        self.db_name = os.path.join(datadir, 'covid-india.db')
        self.conn = self.make_conn()
        
    def init_tables(self):
        self.tables = {}

    def make_conn(self):
        conn = sqlite3.connect(self.db_name)
        return conn

    def create_tables(self):
        cursor = self.conn.cursor()
        for table_obj in self.tables.values():
            print(f'Creating table : {table_obj.table_name}')
            create_query = table_obj.create_table()
            cursor.execute(create_query)
            self.conn.commit()

    def insert_row(self, data):
        
        cursor = self.conn.cursor()

        # Insert data in all the relevant tables
        for id, tableobj in self.tables.items():
            if id not in data:
                continue

            vals = data[id]

            if isinstance(vals, dict):
                tableobj.insert_row(cursor=cursor, **vals)
            elif isinstance(vals, list):
                for valitem in vals:
                    tableobj.insert_row(cursor=cursor, **valitem)

        self.conn.commit()
