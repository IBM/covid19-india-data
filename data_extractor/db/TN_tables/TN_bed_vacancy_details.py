import sqlite3
from .db import DB

class DistrictHospitalBedDetailsTable(DB):
    def __init__(self):
        self.table_name = "TN_district_hospital_bed_details"
        self.table_desc = "Tamil Nadu hospital bed district wise details, table on pages 7, 8 and 9"
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'district': 'STRING NOT NULL',
            'total_covid_o2': 'INT',
            'total_covid_non_o2': 'INT',
            'total_covid_icu': 'INT',
            'today_occupancy_o2': 'INT',
            'today_occupancy_non_o2': 'INT',
            'today_occupancy_icu': 'INT',
            'total_vacancy_o2': 'INT',
            'total_vacancy_non_o2': 'INT',
            'total_vacancy_icu': 'INT',
            'total_vacancy': 'INT',
            'embarked_covid_beds': 'INT',
            'embarked_covid_occupancy': 'INT',
            'embarked_covid_vacancy': 'INT',
            'iccc_proposed_rural': 'INT',
            'iccc_beds_proposed_rural': 'INT',
            'iccc_total_beds_available_rural': 'INT',
            'iccc_beds_occupied_rural': 'INT',
            'iccc_proposed_urban': 'INT',
            'iccc_beds_urban': 'INT'
        }

        return cols

    def create_table(self):
        colstr = [f'{column_name} {column_type}' for column_name, column_type in self.cols.items()]
        colstr = ', '.join(colstr)
        query = f"CREATE TABLE IF NOT EXISTS `{self.table_name}` ({colstr}, PRIMARY KEY (date, district))"
        return query
