import sqlite3

from .db import Database
from .HR_tables import HR_caseinfo

class HaryanaDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'case-information': HR_caseinfo.CaseInformation()
        }
        