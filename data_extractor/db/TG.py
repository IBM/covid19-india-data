import sqlite3

from .db import Database
from .TG_tables import TG_symptomatic, TG_comorbidities, TG_agedist

class TelanganaDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'asymptomatic-status': TG_symptomatic.SymptomaticCases(),
            'comorbidities-fatality': TG_comorbidities.ComorbiditiesFatalityCount(),
            'agewise-info': TG_agedist.AgeGenderDist()
        }
        