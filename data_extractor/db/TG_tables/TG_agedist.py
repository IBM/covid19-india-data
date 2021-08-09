import sqlite3
from .db import DB


class AgeGenderDist(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'TG_age_gender_dist'
        self.table_desc = 'Telangana age and gender distribution of positive cases'
        self.cols = self.getcolumns()

    def getcolumns(self):

        cols = {
            'date': 'DATE NOT NULL PRIMARY KEY',
            'ages_11_to_20_female': 'FLOAT',
            'ages_11_to_20_male': 'FLOAT',
            'ages_11_to_20_total': 'FLOAT',
            'ages_21_to_30_female': 'FLOAT',
            'ages_21_to_30_male': 'FLOAT',
            'ages_21_to_30_total': 'FLOAT',
            'ages_31_to_40_female': 'FLOAT',
            'ages_31_to_40_male': 'FLOAT',
            'ages_31_to_40_total': 'FLOAT',
            'ages_41_to_50_female': 'FLOAT',
            'ages_41_to_50_male': 'FLOAT',
            'ages_41_to_50_total': 'FLOAT',
            'ages_51_to_60_female': 'FLOAT',
            'ages_51_to_60_male': 'FLOAT',
            'ages_51_to_60_total': 'FLOAT',
            'ages_61_to_70_female': 'FLOAT',
            'ages_61_to_70_male': 'FLOAT',
            'ages_61_to_70_total': 'FLOAT',
            'ages_71_to_80_female': 'FLOAT',
            'ages_71_to_80_male': 'FLOAT',
            'ages_71_to_80_total': 'FLOAT',
            'ages_81_and_above_female': 'FLOAT',
            'ages_81_and_above_male': 'FLOAT',
            'ages_81_and_above_total': 'FLOAT',
            'ages_upto_10_female': 'FLOAT',
            'ages_upto_10_male': 'FLOAT',
            'ages_upto_10_total': 'FLOAT',
            'total_female': 'FLOAT',
            'total_male': 'FLOAT',
            'total_total': 'FLOAT'
        }

        return cols
