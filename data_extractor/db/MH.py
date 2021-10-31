import sqlite3

from .db import Database
from .MH_tables import MH_corporation_info, MH_district_info


class MaharashtraDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'active-case-info': MH_district_info.DistrictInformation(),
            'district-case-info': MH_corporation_info.CorporationInformation()
        }
        