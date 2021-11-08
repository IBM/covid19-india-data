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
    from local_extractor.states.state_utils import UK_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils
    from states.state_utils import UK_utils


class UttarakhandExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        self.nums_regex = re.compile(r'([\d,+-]+)[ ]*\(([\d,+-]+)\)')

    def extract_district_testing_info(self, tables):

        # Identify case info table
        keywords = {'district', 'samples', 'negative', 'positive', 'cumulative', 'awaited'}

        datatable = common_utils.find_table_by_keywords(tables, keywords)
        if datatable is None:
            return None

        datalist = UK_utils.process_district_testing_table(datatable)

        for datadict in datalist:
            datadict['date'] = self.date

        return datalist

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
        for idx, row in enumerate(df_record_list[1:]):
            result.append({
                'date': self.date,
                'district': row[0],
                'cases_total': UK_utils.str2int(row[1]),
                'recovered_total': UK_utils.str2int(row[2]),
                'active_cases': UK_utils.str2int(row[3]),
                'deaths_total': UK_utils.str2int(row[4]),
                'migrated_total': UK_utils.str2int(row[5])
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

    """
    ## Commenting this block since very few bulletins provide this information
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
    """

    def extract_district_mucormycosis_cases_info(self, tables):

        keywords = {'district', 'hospital', 'today', 'cumulative'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)
        old_format = False

        if datatable is not None:
            old_format = False
        else:
            # New format table not found. Try with the older format
            old_format = True
            keywords = {'district', 'hospital', 'total', 'death', 'discharge'}
            datatable = common_utils.find_table_by_keywords(tables, keywords)
            
        if datatable is None:
            return None

        datalist = UK_utils.process_mucormycosis_table(datatable, old_format)
        
        for datadict in datalist:
            datadict['date'] = self.date

        return datalist


    def process_col_ids_to_parse(self, df):
        for col_id, col_name in enumerate(df.iloc[0]):
            df.iloc[0][col_id] = df.iloc[0][col_id].replace("\n", "")
            if not col_name and col_id > 1:
                if df.iloc[0][col_id-1][-2] != "_":
                    df.iloc[0][col_id-1] += "_1"
                df.iloc[0][col_id] = df.iloc[0][col_id-1][:-1] + str(int(df.iloc[0][col_id-1][-1]) + 1)

        col_ids_to_parse = {

            'HCW_24h_col_id': None,
            'HCW_dose1_total_col_id': None,
            'HCW_dose2_total_col_id': None,

            'FLW_24h_col_id': None,
            'FLW_dose1_total_col_id': None,
            'FLW_dose2_total_col_id': None,

            'citizen_24h_col_id': None,
            'citizen_60_plus_24h_col_id': None,
            'citizen_60_plus_dose1_total_col_id': None,
            'citizen_45_to_59_24h_col_id': None,
            'citizen_45_to_59_dose1_total_col_id': None,
            'citizen_45_plus_dose1_total_col_id': None,
            'citizen_45_plus_dose2_total_col_id': None,
            'citizen_18_to_44_dose1_total_col_id': None,
            'citizen_18_to_44_dose2_total_col_id': None,

            'sessions_24h_col_id': None,
            'sessions_total_col_id': None,
        }

        # if health worker found - 2021-02-08 onwards
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'care' in col_name.lower():
                if col_name[-1] == '1':
                    col_ids_to_parse['HCW_24h_col_id'] = col_id
                elif col_name[-1] == '2':
                    col_ids_to_parse['HCW_dose1_total_col_id'] = col_id
                elif col_name[-1] == '3':
                    col_ids_to_parse['HCW_dose2_total_col_id'] = col_id

        # if front line found - 2021-02-08 onwards
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'line' in col_name.lower():
                if col_name[-1] == '1':
                    col_ids_to_parse['FLW_24h_col_id'] = col_id
                elif col_name[-1] == '2':
                    col_ids_to_parse['FLW_dose1_total_col_id'] = col_id
                elif col_name[-1] == '3':
                    col_ids_to_parse['FLW_dose2_total_col_id'] = col_id

        # if citizen found - 2021-04-05 onwards
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'citizen' in col_name.lower():
                if col_name[-1] == '1':
                    col_ids_to_parse['citizen_24h_col_id'] = col_id
                elif col_name[-1] == '2':
                    col_ids_to_parse['citizen_45_plus_dose1_total_col_id'] = col_id
                elif col_name[-1] == '3':
                    col_ids_to_parse['citizen_45_plus_dose2_total_col_id'] = col_id
                elif col_name[-1] == '4':
                    col_ids_to_parse['citizen_18_to_44_dose1_total_col_id'] = col_id
                elif col_name[-1] == '5':
                    col_ids_to_parse['citizen_18_to_44_dose2_total_col_id'] = col_id

        # remember 03-01, 03-02, 03-08, 04-04
        # if 60+ found
        # if 45 found
        if not col_ids_to_parse['citizen_24h_col_id']:
            for col_id, col_name in enumerate(df.iloc[0]):

                if '60+' in col_name.lower():
                    if col_name[-1] == '1':
                        col_ids_to_parse['citizen_60_plus_24h_col_id'] = col_id
                    elif col_name[-1] == '2':
                        col_ids_to_parse['citizen_60_plus_dose1_total_col_id'] = col_id

                if '45-' in col_name.lower():
                    if col_name[-1] == '1':
                        col_ids_to_parse['citizen_45_to_59_24h_col_id'] = col_id
                    elif col_name[-1] == '2':
                        col_ids_to_parse['citizen_45_to_59_dose1_total_col_id'] = col_id

            # TODO: if above two found, use their col_id to populate
            #  citizen_45_plus_dose1_total_col_id and citizen_45_plus_dose2_total_col_id

        # if session held today found
        # if session held cumulative found
        for col_id, col_name in enumerate(df.iloc[0]):
            if 'session' in col_name.lower():
                if 'today' in col_name.lower():
                    col_ids_to_parse['sessions_24h_col_id'] = col_id
                elif 'cumulative' in col_name.lower():
                    col_ids_to_parse['sessions_total_col_id'] = col_id

        # if vaccinated today found - till 2021-02-07 - only health workers
        if not col_ids_to_parse['HCW_24h_col_id']:
            for col_id, col_name in enumerate(df.iloc[0]):
                if 'vaccinated' in col_name.lower():
                    if 'today' in col_name.lower():
                        col_ids_to_parse['HCW_24h_col_id'] = col_id
                    elif 'cumulative' in col_name.lower():
                        col_ids_to_parse['HCW_dose1_total_col_id'] = col_id

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

        if col_ids_to_parse['HCW_24h_col_id']:
            del df_record_list[1]

        for idx, row in enumerate(df_record_list[1:]):

            tmp = {
                'date': self.date,
                'district_name': row[0],

                'sessions_24h': row[col_ids_to_parse['sessions_24h_col_id']] if col_ids_to_parse['sessions_24h_col_id'] else None,
                'sessions_total': row[col_ids_to_parse['sessions_24h_col_id']] if col_ids_to_parse['sessions_total_col_id'] else None,

                'citizen_24h': row[col_ids_to_parse['citizen_24h_col_id']] if col_ids_to_parse['citizen_24h_col_id'] else None,
                'citizen_60_plus_24h': row[col_ids_to_parse['citizen_60_plus_24h_col_id']] if col_ids_to_parse['citizen_60_plus_24h_col_id'] else None,
                'citizen_60_plus_dose1_total': row[col_ids_to_parse['citizen_60_plus_dose1_total_col_id']] if col_ids_to_parse['citizen_60_plus_dose1_total_col_id'] else None,
                'citizen_45_to_59_24h': row[col_ids_to_parse['citizen_45_to_59_24h_col_id']] if col_ids_to_parse['citizen_45_to_59_24h_col_id'] else None,
                'citizen_45_to_59_dose1_total': row[col_ids_to_parse['citizen_45_to_59_dose1_total_col_id']] if col_ids_to_parse['citizen_45_to_59_dose1_total_col_id'] else None,
                'citizen_45_plus_dose1_total': row[col_ids_to_parse['citizen_45_plus_dose1_total_col_id']] if col_ids_to_parse['citizen_45_plus_dose1_total_col_id'] else None,
                'citizen_45_plus_dose2_total': row[col_ids_to_parse['citizen_45_plus_dose2_total_col_id']] if col_ids_to_parse['citizen_45_plus_dose2_total_col_id'] else None,
                'citizen_18_to_44_dose1_total': row[col_ids_to_parse['citizen_18_to_44_dose1_total_col_id']] if col_ids_to_parse['citizen_18_to_44_dose1_total_col_id'] else None,
                'citizen_18_to_44_dose2_total': row[col_ids_to_parse['citizen_18_to_44_dose2_total_col_id']] if col_ids_to_parse['citizen_18_to_44_dose2_total_col_id'] else None,

                'HCW_24h': row[col_ids_to_parse['HCW_24h_col_id']] if col_ids_to_parse['HCW_24h_col_id'] else None,
                'HCW_dose1_total': row[col_ids_to_parse['HCW_dose1_total_col_id']] if col_ids_to_parse['HCW_dose1_total_col_id'] else None,
                'HCW_dose2_total': row[col_ids_to_parse['HCW_dose2_total_col_id']] if col_ids_to_parse['HCW_dose2_total_col_id'] else None,

                'FLW_24h': row[col_ids_to_parse['FLW_24h_col_id']] if col_ids_to_parse['FLW_24h_col_id'] else None,
                'FLW_dose1_total': row[col_ids_to_parse['FLW_dose1_total_col_id']] if col_ids_to_parse['FLW_dose1_total_col_id'] else None,
                'FLW_dose2_total': row[col_ids_to_parse['FLW_dose2_total_col_id']] if col_ids_to_parse['FLW_dose2_total_col_id'] else None,

            }

            for k, v in tmp.items():
                if k in ['date', 'district_name'] or v is None:
                    continue
                tmp[k] = UK_utils.str2int(v)

            result.append(tmp)

        return result

    def extract(self):

        n = common_utils.n_pages_in_pdf(self.report_fpath)

        all_tables = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, split_text=False)

        district_testing = self.extract_district_testing_info(all_tables)
        district_cases = self.extract_district_cases_info(all_tables)
        # hospital_deaths = self.extract_hospital_deaths_info(all_tables)
        district_mucormycosis_cases = self.extract_district_mucormycosis_cases_info(all_tables)
        district_vaccination = self.extract_district_vaccination_cases_info(all_tables)

        result = {
            'district-testing': district_testing,
            'district-cases': district_cases,
            'district-mucormycosis-cases': district_mucormycosis_cases,
            'district-vaccination': district_vaccination,
            # 'hospital-deaths': hospital_deaths,
        }

        return result


if __name__ == '__main__':
    date = '01-may-2021'
    path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore_UK/bulletins/UK/UK-Bulletin-2021-02-10.pdf"
    # path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore_UK/bulletins/UK/UK-Bulletin-2021-03-09.pdf"
    # path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore_UK/bulletins/UK/UK-Bulletin-2020-10-01.pdf"
    obj = UttarakhandExtractor(date, path)
    obj.extract()
