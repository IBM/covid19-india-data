import sqlite3

from .db import Database
from .TN_tables import TN_case_info, TN_detailed_cases, TN_district_detailed_cases, TN_bed_vacancy_details, \
    TN_detailed_deaths, TN_incoming_passengers_testing, TN_airport_surveillance, TN_flight_surveillance, \
    TN_railway_surveillance, TN_seaport_surveillance, TN_individual_case_info

class TamilNaduDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'case-info': TN_case_info.CumulativeInfoTable(),
            'detailed-info': TN_detailed_cases.DetailedInfoTable(),
            'district-info': TN_district_detailed_cases.DistrictDetailsTable(),
            'district-bed-info': TN_bed_vacancy_details.DistrictHospitalBedDetailsTable(),
            'death-info': TN_detailed_deaths.DeathMorbiditiesTable(),
            'travel-info': TN_incoming_passengers_testing.IncomingPassengersTable(),
            'airport': TN_airport_surveillance.AirportSurveillanceTable(),
            'flights': TN_flight_surveillance.FlightSurveillanceTable(),
            'trains': TN_railway_surveillance.RailwaySurveillanceTable(),
            'ships': TN_seaport_surveillance.SeaportSurveillanceTable(),
            'individual-case-info': TN_individual_case_info.IndividualCaseInfo()
        }

    def insert_row(self, data):
        cursor = self.conn.cursor()

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
