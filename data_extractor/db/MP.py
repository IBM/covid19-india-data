import sqlite3

from .db import Database
from .MP_tables import (
    MP_overview,
    VaccinationCoverage,
)


class MadhyaPradeshDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'overview': MP_overview.Overview(),
            'vaccination-coverage': MP_vaccination_coverage.VaccinationCoverage(),
        }
        