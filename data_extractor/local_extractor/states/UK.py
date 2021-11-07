import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import json
import pandas as pd
import camelot

import pdfminer
from pdfminer.high_level import extract_pages

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class UttarakhandExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        self.nums_regex = re.compile(r'([\d,+-]+)[ ]*\(([\d,+-]+)\)')

    def process_district_testing_df(self, df):
        df = df.replace('-', None)
        for col_id, col_name in enumerate(df.iloc[1]):
            if col_name:
                df.iloc[0][col_id] = col_name
        df = df.drop([1]).reset_index(drop=True)
        return df.to_dict(orient='records')

    def extract_district_testing_info(self, tables):

        # Identify case info table
        keywords = {'district', 'samples', 'negative', 'positive', 'cumulative', 'awaited'}

        case_info_table = common_utils.find_table_by_keywords(tables, keywords)
        if case_info_table is None:
            return None

        # Extract information from relevant columns
        df_record_list = self.process_district_testing_df(case_info_table)
        result = []
        for row in df_record_list[1:-1]:
            result.append({
                'date': self.date,
                'district': row[0],  # df['Districts'],
                'samples_tested_today': row[1],  # df['Samples Sent to Labs Today'],
                'negative_results_24h': row[2],  # df['Negative in last 24 hours'],
                'negative_results_total': row[3],  # df['Negative Cumulative (including Pvt. Lab)'],
                'positive_results_24h': row[4],  # df['Positive in last 24 hours'],
                'positive_results_total': row[5],  # df['Positive Cumulative (including Pvt. Lab)'],
                'samples_tested_total': row[6],  # df['Cumulative Samples Tested'],
                'samples_results_awaited': row[7],  # df['Results Awaited (including sample sent to labs today)'
            })

        return result

    def extract_district_cases_info(self, tables):

        # Identify case info table
        keywords = {'district', 'cases', 'treated', 'active', 'deaths', 'migrated'}

        district_case_info_table = common_utils.find_table_by_keywords(tables, keywords)
        if district_case_info_table is None:
            return None

        # Extract information from relevant columns
        district_case_info_table = district_case_info_table.replace('-', None)
        df_record_list = district_case_info_table.to_dict(orient='records')
        result = []
        for idx, row in enumerate(df_record_list[1:-1]):
            result.append({
                'date': self.date,
                'district': row[0],
                'cases_total': row[1],
                'recovered_total': row[2],
                'active_cases': row[3],
                'deaths_total': row[4],
                'migrated_total': row[5]
            })

        return result

    def process_hospital_deaths_df(self, df):
        df_record_list = df.to_dict(orient='records')
        for idx, row in enumerate(df_record_list[1:-1]):
            if not row[0]:
                row[0] = df_record_list[idx][0]
            for k, v in row.items():
                if v == "-":
                    row[k] = None

        return df_record_list

    def extract_hospital_deaths_info(self, tables):

        # Identify case info table
        keywords = {'district', 'cumulative', 'hospital', 'death'}

        hospital_death_info_table = common_utils.find_table_by_keywords(tables, keywords)
        if hospital_death_info_table is None:
            return None

        # Extract information from relevant columns
        df_record_list = self.process_hospital_deaths_df(hospital_death_info_table)
        result = []
        for idx, row in enumerate(df_record_list[1:-1]):
            result.append({
                'date': self.date,
                'district': row[0],
                'hospital_name': row[2],
                'deaths_new': row[3]
            })

        return result

    def process_district_mucormycosis_cases_new_df(self, df):
        for col_id, col_name in enumerate(df.iloc[0]):
            if not col_name and col_id > 1:
                df.iloc[0][col_id] = df.iloc[0][col_id-1]
            if df.iloc[1][col_id]:
                df.iloc[0][col_id] += " " + df.iloc[1][col_id]

        df = df.drop([1]).reset_index(drop=True)
        # df = df.replace('-', None)
        return self.process_district_mucormycosis_cases_old_df(df, 0)

    def process_district_mucormycosis_cases_old_df(self, df, fill_row_id=1):
        df_record_list = df.to_dict(orient='records')
        for idx, row in enumerate(df_record_list[1:-1]):
            if not row[fill_row_id]:
                row[fill_row_id] = df_record_list[idx][fill_row_id]
            for k, v in row.items():
                if v == "-":
                    row[k] = None
        return df_record_list

    def extract_district_mucormycosis_cases_info(self, tables):

        # Identify case info table
        keywords = {'district', 'hospital', 'today', 'cumulative'}

        district_mucormycosis_cases_info_table = common_utils.find_table_by_keywords(tables, keywords)
        if district_mucormycosis_cases_info_table is None:

            keywords = {'district', 'hospital', 'total', 'death', 'discharge'}

            district_mucormycosis_cases_info_table = common_utils.find_table_by_keywords(tables, keywords)
            if district_mucormycosis_cases_info_table is None:
                return None

            # Extract information from relevant columns
            df_record_list = self.process_district_mucormycosis_cases_old_df(district_mucormycosis_cases_info_table)
            result = []
            for idx, row in enumerate(df_record_list[1:-1]):

                result.append({
                    'date': self.date,
                    'district': row[1],
                    'hospital_name': row[2],
                    'cases_new': 0,
                    'deaths_new': 0,
                    'discharged_new': 0,
                    'cases_total': row[3],
                    'deaths_total': row[4],
                    'discharged_total': row[5],
                    'migrated_total': 0
                })

            return result

        else:
            # Extract information from relevant columns
            df_record_list = self.process_district_mucormycosis_cases_new_df(district_mucormycosis_cases_info_table)
            result = []
            for idx, row in enumerate(df_record_list[1:-1]):
                result.append({
                    'date': self.date,
                    'district': row[0],
                    'hospital_name': row[1],
                    'cases_new': row[2],
                    'deaths_new': row[3],
                    'discharged_new': row[4],
                    'cases_total': row[5],
                    'deaths_total': row[6],
                    'discharged_total': row[7],
                    'migrated_total': row[8]
                })

            return result

    def process_col_ids_to_parse(self, df):
        for col_id, col_name in enumerate(df.iloc[0]):
            df.iloc[0][col_id] = df.iloc[0][col_id].replace("\n", "")
            if not col_name and col_id > 1:
                if df.iloc[0][col_id-1][-2] != "_":
                    df.iloc[0][col_id-1] += "_1"
                df.iloc[0][col_id] = df.iloc[0][col_id-1][:-1] + str(int(df.iloc[0][col_id-1][-1]) + 1)

        col_ids_to_parse = {

            'health_care_worker_24h_col_id': None,
            'health_care_worker_first_dose_total_col_id': None,
            'health_care_worker_second_dose_total_col_id': None,

            'front_line_worker_24h_col_id': None,
            'front_line_worker_first_dose_total_col_id': None,
            'front_line_worker_second_dose_total_col_id': None,

            'citizen_24h_col_id': None,
            'citizen_60_plus_24h_col_id': None,
            'citizen_60_plus_first_dose_total_col_id': None,
            'citizen_45_to_59_24h_col_id': None,
            'citizen_45_to_59_first_dose_total_col_id': None,
            'citizen_45_plus_first_dose_total_col_id': None,
            'citizen_45_plus_second_dose_total_col_id': None,
            'citizen_18_to_44_first_dose_total_col_id': None,
            'citizen_18_to_44_second_dose_total_col_id': None,

            'sessions_24h_col_id': None,
            'sessions_total_col_id': None,
        }

        # if health worker found - 2021-02-08 onwards
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'care' in col_name.lower():
                if col_name[-1] == '1':
                    col_ids_to_parse['health_care_worker_24h_col_id'] = col_id
                elif col_name[-1] == '2':
                    col_ids_to_parse['health_care_worker_first_dose_total_col_id'] = col_id
                elif col_name[-1] == '3':
                    col_ids_to_parse['health_care_worker_second_dose_total_col_id'] = col_id

        # if front line found - 2021-02-08 onwards
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'line' in col_name.lower():
                if col_name[-1] == '1':
                    col_ids_to_parse['front_line_worker_24h_col_id'] = col_id
                elif col_name[-1] == '2':
                    col_ids_to_parse['front_line_worker_first_dose_total_col_id'] = col_id
                elif col_name[-1] == '3':
                    col_ids_to_parse['front_line_worker_second_dose_total_col_id'] = col_id

        # if citizen found - 2021-04-05 onwards
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'citizen' in col_name.lower():
                if col_name[-1] == '1':
                    col_ids_to_parse['citizen_24h_col_id'] = col_id
                elif col_name[-1] == '2':
                    col_ids_to_parse['citizen_45_plus_first_dose_total_col_id'] = col_id
                elif col_name[-1] == '3':
                    col_ids_to_parse['citizen_45_plus_second_dose_total_col_id'] = col_id
                elif col_name[-1] == '4':
                    col_ids_to_parse['citizen_18_to_44_first_dose_total_col_id'] = col_id
                elif col_name[-1] == '5':
                    col_ids_to_parse['citizen_18_to_44_second_dose_total_col_id'] = col_id

        # remember 03-01, 03-02, 03-08, 04-04
        # if 60+ found
        # if 45 found
        if not col_ids_to_parse['citizen_24h_col_id']:
            for col_id, col_name in enumerate(df.iloc[0]):

                if '60+' in col_name.lower():
                    if col_name[-1] == '1':
                        col_ids_to_parse['citizen_60_plus_24h_col_id'] = col_id
                    elif col_name[-1] == '2':
                        col_ids_to_parse['citizen_60_plus_first_dose_total_col_id'] = col_id

                if '45-' in col_name.lower():
                    if col_name[-1] == '1':
                        col_ids_to_parse['citizen_45_to_59_24h_col_id'] = col_id
                    elif col_name[-1] == '2':
                        col_ids_to_parse['citizen_45_to_59_first_dose_total_col_id'] = col_id

            # TODO: if above two found, use their col_id to populate
            #  citizen_45_plus_first_dose_total_col_id and citizen_45_plus_second_dose_total_col_id

        # if session held today found
        # if session held cumulative found
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'session' in col_name.lower():
                if 'today' in col_name.lower():
                    col_ids_to_parse['sessions_24h_col_id'] = col_id
                elif 'cumulative' in col_name.lower():
                    col_ids_to_parse['sessions_total_col_id'] = col_id

        # if vaccinated today found - till 2021-02-07 - only health workers
        if not col_ids_to_parse['health_care_worker_24h_col_id']:
            for col_id, col_name in enumerate(df.iloc[0]):
                if 'vaccinated' in col_name.lower():
                    if 'today' in col_name.lower():
                        col_ids_to_parse['health_care_worker_24h_col_id'] = col_id
                    elif 'cumulative' in col_name.lower():
                        col_ids_to_parse['health_care_worker_first_dose_total_col_id'] = col_id

        return col_ids_to_parse

    def extract_district_vaccination_cases_info(self, tables):

        # Identify case info table
        keywords = {'district', 'vaccinated'}

        district_vaccination_cases_info_table = common_utils.find_table_by_keywords(tables, keywords)

        if district_vaccination_cases_info_table is None:
            return None

        result = []

        df_record_list = district_vaccination_cases_info_table.to_dict(orient='records')

        col_ids_to_parse = self.process_col_ids_to_parse(district_vaccination_cases_info_table)

        if col_ids_to_parse['health_care_worker_24h_col_id']:
            del df_record_list[1]

        for idx, row in enumerate(df_record_list[1:-1]):

            result.append({
                'date': self.date,
                'district': row[0],

                'sessions_24h': row[col_ids_to_parse['sessions_24h_col_id']] if col_ids_to_parse['sessions_24h_col_id'] else 0,
                'sessions_total': row[col_ids_to_parse['sessions_24h_col_id']] if col_ids_to_parse['sessions_total_col_id'] else 0,

                'citizen_24h': row[col_ids_to_parse['citizen_24h_col_id']] if col_ids_to_parse['citizen_24h_col_id'] else 0,
                'citizen_60_plus_24h': row[col_ids_to_parse['citizen_60_plus_24h_col_id']] if col_ids_to_parse['citizen_60_plus_24h_col_id'] else 0,
                'citizen_60_plus_first_dose_total': row[col_ids_to_parse['citizen_60_plus_first_dose_total_col_id']] if col_ids_to_parse['citizen_60_plus_first_dose_total_col_id'] else 0,
                'citizen_45_to_59_24h': row[col_ids_to_parse['citizen_45_to_59_24h_col_id']] if col_ids_to_parse['citizen_45_to_59_24h_col_id'] else 0,
                'citizen_45_to_59_first_dose_total': row[col_ids_to_parse['citizen_45_to_59_first_dose_total_col_id']] if col_ids_to_parse['citizen_45_to_59_first_dose_total_col_id'] else 0,
                'citizen_45_plus_first_dose_total': row[col_ids_to_parse['citizen_45_plus_first_dose_total_col_id']] if col_ids_to_parse['citizen_45_plus_first_dose_total_col_id'] else 0,
                'citizen_45_plus_second_dose_total': row[col_ids_to_parse['citizen_45_plus_second_dose_total_col_id']] if col_ids_to_parse['citizen_45_plus_second_dose_total_col_id'] else 0,
                'citizen_18_to_44_first_dose_total': row[col_ids_to_parse['citizen_18_to_44_first_dose_total_col_id']] if col_ids_to_parse['citizen_18_to_44_first_dose_total_col_id'] else 0,
                'citizen_18_to_44_second_dose_total': row[col_ids_to_parse['citizen_18_to_44_second_dose_total_col_id']] if col_ids_to_parse['citizen_18_to_44_second_dose_total_col_id'] else 0,

                'health_care_worker_24h': row[col_ids_to_parse['health_care_worker_24h_col_id']] if col_ids_to_parse['health_care_worker_24h_col_id'] else 0,
                'health_care_worker_first_dose_total': row[col_ids_to_parse['health_care_worker_first_dose_total_col_id']] if col_ids_to_parse['health_care_worker_first_dose_total_col_id'] else 0,
                'health_care_worker_second_dose_total': row[col_ids_to_parse['health_care_worker_second_dose_total_col_id']] if col_ids_to_parse['health_care_worker_second_dose_total_col_id'] else 0,

                'front_line_worker_24h': row[col_ids_to_parse['front_line_worker_24h_col_id']] if col_ids_to_parse['front_line_worker_24h_col_id'] else 0,
                'front_line_worker_first_dose_total': row[col_ids_to_parse['front_line_worker_first_dose_total_col_id']] if col_ids_to_parse['front_line_worker_first_dose_total_col_id'] else 0,
                'front_line_worker_second_dose_total': row[col_ids_to_parse['front_line_worker_second_dose_total_col_id']] if col_ids_to_parse['front_line_worker_second_dose_total_col_id'] else 0,

            })

        return result

    def extract(self):

        n = common_utils.n_pages_in_pdf(self.report_fpath)

        all_tables = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, strip_text="", split_text=False)

        district_testing = self.extract_district_testing_info(all_tables)
        district_cases = self.extract_district_cases_info(all_tables)
        hospital_deaths = self.extract_hospital_deaths_info(all_tables)
        district_mucormycosis_cases = self.extract_district_mucormycosis_cases_info(all_tables)
        district_vaccination = self.extract_district_vaccination_cases_info(all_tables)

        result = {
            'district-testing': district_testing,
            'district-cases': district_cases,
            'hospital-deaths': hospital_deaths,
            'district-mucormycosis-cases': district_mucormycosis_cases,
            'district-vaccination': district_vaccination,
        }

        return result


if __name__ == '__main__':
    date = '01-may-2021'
    path = "all_data/bulletins/UK/UK-Bulletin-2021-10-01.pdf"
    obj = UttarakhandExtractor(date, path)
