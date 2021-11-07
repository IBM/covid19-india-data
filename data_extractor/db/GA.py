import sqlite3

from .db import Database
from .GA_tables import (
    GA_overview,
    GA_active_cases, 
    GA_bed_capacity,
)


class GoaDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'overview': GA_overview.Overview(),
            'active-cases': GA_active_cases.ActiveCases(),
            'bed-capacity': GA_bed_capacity.BedCapacity(),
        }
        