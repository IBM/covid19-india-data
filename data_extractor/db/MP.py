import sqlite3

from .db import Database
from .MP_tables import (
    MP_overview,
    MP_district_info,
    MP_calls,
    MP_centers,
    MP_teams,
    MP_testing,
    MP_vaccination_coverage,
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
            'district-info': MP_district_info.DistrictInfo(),
            'calls': MP_calls.Calls(),
            'centers': MP_centers.Centers(),
            'teams': MP_teams.Teams(),
            'testing': MP_testing.Testing(),
            'vaccination-coverage': MP_vaccination_coverage.VaccinationCoverage(),
        }
        