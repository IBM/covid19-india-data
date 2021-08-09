import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
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


class WestBengalExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath
        
        self.nums_regex = re.compile(r'([\d,+-]+)[ ]*\(([\d,+-]+)\)')

    def _process_case_nums_(self, datadict, colname, new_cols, del_old=False):
        if colname in datadict:
            m = self.nums_regex.match(datadict[colname])
            if m:
                grps = m.groups()
                datadict[new_cols[0]] = grps[0]
                datadict[new_cols[1]] = grps[1]

        if del_old:
            del datadict[colname]

        return datadict

    def _process_district_case_nums_(self, num):
        
        num = num.strip()
        num_split = re.split('[+\-]+', num)
        plus_in_num = '+' in num
        neg_in_num = '-' in num
        
        if not plus_in_num and not neg_in_num:
            total = locale.atoi(num_split[0])
            new = 0
        else:
            total, new = num_split
            total = locale.atoi(total)
            new = locale.atoi(new)
            if neg_in_num:
                new = -1 * new
        
        return total, new

    def extract_case_info(self, tables):

        # Identify case info table
        caseinfo_table = None
        keywords = {'new', 'cases', 'total', 'discharged', 'active', 'discharge'}

        caseinfo_table = common_utils.find_table_by_keywords(tables, keywords)        
        if caseinfo_table is None:
            return None

        # Extract information from relevant columns
        df_dict = common_utils.convert_df_to_dict(caseinfo_table, key_idx=1, val_idx=2)
        keymap = {
            'cases_new': ['new', 'case'],
            'cases_total': ['total', 'case'],
            'discharged_total': ['total', 'discharged'],
            'deaths_total': ['total', 'deaths'],
            'cases_active': ['active', 'cases'],
            'discharge_rate': ['discharge', 'rate'],
            'fatality_rate': ['fatality', 'rate']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # Clean result
        result = self._process_case_nums_(result, 'discharged_total', ['discharged_total', 'discharged_new'])
        result = self._process_case_nums_(result, 'deaths_total', ['deaths_total', 'deaths_new'])
        result = self._process_case_nums_(result, 'cases_active', ['cases_active_total', 'cases_active_new'], True)

        atoi_cols = ['cases_total', 'cases_new', 'discharged_total', 'discharged_new', 
                    'deaths_total', 'deaths_new', 'cases_active_total', 'cases_active_new']
        for col in atoi_cols:
            if col in result:
                result[col] = locale.atoi(result[col])
        
        if 'discharge_rate' in result:
            result['discharge_rate'] = float(common_utils.clean_numbers_str(result['discharge_rate']))

        return result

    def extract_quarantine_info(self, tables):

        # Identify quarantine tables
        quarantine_table = None
        keywords = {'home', 'patients', 'people'}

        quarantine_table = common_utils.find_table_by_keywords(tables, keywords)
        if quarantine_table is None:
            return None
        
        cols = quarantine_table.shape[1]
        df_dict = common_utils.convert_df_to_dict(quarantine_table, key_idx=cols-2, val_idx=cols-1)
        keymap = {
            'total_patients_home_isolation': ['total', 'home', 'quarantine', 'people'],
            'current_patients_home_isolation': ['total', 'people', 'currently in home'],
            'released_patients_home_isolation': ['total', 'released', 'home'],
            'n_safe_homes': ['number of safe home'],
            'safe_home_beds': ['number', 'beds', 'safe', 'home'],
            'current_patients_hospital': ['total', 'patients', 'hospital'],
            'current_patients_safe_homes': ['total', 'patients', 'safe', 'home']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        
        for k in result.keys():
            result[k] = locale.atoi(result[k])
        result['date'] = self.date
        return result

    def extract_hospital_infra_info(self, tables):

        # Identify hospital info table
        hospitalinfo_table = None
        keywords = {'hospitals', 'treating', 'icu', 'beds'}

        hospitalinfo_table = common_utils.find_table_by_keywords(tables, keywords)        
        if hospitalinfo_table is None:
            return None

        # Extract information from relevant columns
        df_dict = common_utils.convert_df_to_dict(hospitalinfo_table, key_idx=1, val_idx=2)
        keymap = {
            'hospital_dedicated': ['number of hospital', 'total'],
            'hospital_dedicated_govt': ['govt', 'hospital', 'total', 'number'],
            'hospital_dedicated_pvt': ['pvt', 'hospital', 'total', 'number'],
            'covid19_beds': ['earmarked', 'beds', 'covid'],
            'covid19_bed_occupancy': ['occupancy', 'beds'],
            'icu_hdu_beds': ['icu', 'beds'],
            'n_safe_homes': ['number of safe home'],
            'safe_home_beds': ['beds', 'safe', 'home', 'number'],       # TODO: Fix for consistency. Also extract home-isolation details here
            'n_ventilators': ['number', 'ventilators']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # Clean result
        if 'covid19_bed_occupancy' in result:
            result['covid19_bed_occupancy'] = float(common_utils.clean_numbers_str(result['covid19_bed_occupancy']))

        for k in keymap.keys():
            if k in result and k not in ['covid19_bed_occupancy']:
                result[k] = locale.atoi(result[k])

        return result

    def extract_hospital_and_quarantine_info(self, tables_tabula, tables_camelot):

        quarantine_info = self.extract_quarantine_info(tables_tabula)
        hospital_info = self.extract_hospital_infra_info(tables_camelot)

        if quarantine_info is None and hospital_info is None:
            return None
        elif quarantine_info is None:
            return hospital_info
        elif hospital_info is None:
            return quarantine_info

        # Both have values. Merge keys and send result
        result = {}
        keys1 = set(hospital_info.keys())
        keys2 = set(quarantine_info.keys())
        all_keys = keys1.union(keys2)

        for key in all_keys:
            result[key] = hospital_info.get(key, None) or quarantine_info.get(key, None)
        
        return result

    def extract_testing_info(self, tables):

        # Identify testing info table
        testing_table = None
        keywords = {'samples', 'test', 'laboratories'}
        testing_table = common_utils.find_table_by_keywords(tables, keywords)

        if testing_table is None:
            return None

        # Extract information from relevant columns
        df_dict = common_utils.convert_df_to_dict(testing_table, key_idx=1, val_idx=2)
        keymap = {
            'samples_tested_today': ['samples tested on'],
            'total_samples_tested': ['total', 'number', 'samples', 'tested'],
            'positivity_rate': ['positivity', 'rate'],
            'tests_per_million': ['test', 'per', 'million'],
            'n_testing_labs': ['total', 'testing', 'laboratories'],
            'rtpcr_antigen_ratio': ['test', 'ratio']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # Clean result
        if 'rtpcr_antigen_ratio' in result:
            val = result['rtpcr_antigen_ratio'].split(':')[0]
            val = int(val) / 100.0
            result['rtpcr_antigen_ratio'] = val

        if 'positivity_rate' in result:
            val = float(common_utils.clean_numbers_str(result['positivity_rate']))
            result['positivity_rate'] = val

        for k in keymap.keys():
            if k in result and k not in ['rtpcr_antigen_ratio', 'positivity_rate']:
                result[k] = locale.atoi(result[k])
        
        return result

    def extract_district_wise_info(self, tables):

        if not tables:
            return None
        
        df = tables[0].df
        df = df.iloc[2:]
        n = df.shape[0]
        result = []
        breakloop = False

        for i, row in df.iterrows():

            if breakloop:
                break

            row = [x for x in list(row) if x]

            # Total columns    
            if row[0].strip().lower() == 'total':
                district = row[0].strip().lower()
                total_cases, new_cases = self._process_district_case_nums_(row[-4].strip())
                total_discharged, new_discharged = self._process_district_case_nums_(row[-3].strip())
                total_deaths, new_deaths = self._process_district_case_nums_(row[-2].strip())
                total_active, new_active = self._process_district_case_nums_(row[-1].strip())
                last_reported_case = None
                
                breakloop = True
            else:
                district = row[1].strip().lower()
                total_cases, new_cases = self._process_district_case_nums_(row[2].strip())
                total_discharged, new_discharged = self._process_district_case_nums_(row[3].strip())
                total_deaths, new_deaths = self._process_district_case_nums_(row[4].strip())
                total_active, new_active = self._process_district_case_nums_(row[5].strip())
                last_reported_case = row[6].strip()

            if last_reported_case:
                last_reported_case = common_utils.parse_dates(last_reported_case)

            tmp = {
                'date': self.date,
                'district': district,
                'cases_total': total_cases, 'cases_new': new_cases,
                'discharged_total': total_discharged, 'discharged_new': new_discharged,
                'deaths_total': total_deaths, 'deaths_new': new_deaths,
                'active_cases_total': total_active, 'active_cases_new': new_active,
                'last_reported_case': last_reported_case
            }

            result.append(tmp)

        return result

    def extract_testing_lab_info(self, tables):

        # Identify testing lab tables
        testing_table = None
        keywords = {'name of testing lab', 'samples tested', 'method', 'testing'}
        testing_table = common_utils.find_all_tables_by_keywords(tables, keywords)

        if len(testing_table) == 0:
            return None
        
        testing_table = pd.concat(testing_table)
        result = []

        flag_expanded_tbl = False
        if testing_table.shape[1] == 7:
            flag_expanded_tbl = True

        for i, row in testing_table.iterrows():
            row = list(row)

            if row[0].lower().strip() in ['total', 's. no.']:
                continue
            
            try:
                if flag_expanded_tbl:
                    district = row[2].lower().strip()
                    authority = row[3].lower().strip()
                else:
                    district, authority = None, None

                labname = row[1].lower().strip()
                samples_tested = locale.atoi(row[-3].strip())
                testtype = row[-2].lower().strip()
                functional_wef = row[-1].lower().strip()
            except:
                pass
            else:
                tmp = {
                    'date': self.date,
                    'testing_lab_name': labname,
                    'samples_tested': samples_tested,
                    'testing_method': testtype,
                    'functional_wef': functional_wef,
                    'district': district,
                    'authority': authority
                }
                result.append(tmp)

        return result

    def extract_ppe_info(self, tables):

        # Identify testing lab tables
        ppe_table = None
        keywords = {'ppe', 'n95', 'gloves', 'sanitizer'}
        ppe_table = common_utils.find_all_tables_by_keywords(tables, keywords)

        if len(ppe_table) == 0:
            return None

        ppe_table = ppe_table[0]
        ppe_table = ppe_table.iloc[2:]

        result = []

        for i, row in ppe_table.iterrows():
            try:
                unit = row[1].strip().lower()
                ppe = locale.atoi(row[2].strip())
                n95 = locale.atoi(row[3].strip())
                reusablemask = locale.atoi(row[4].strip())
                disposablemask = locale.atoi(row[5].strip())
                gloves = locale.atoi(row[6].strip())
                sanitizer = locale.atof(row[7].strip())

                tmp = {
                    'date': self.date,
                    'unit_name': unit,
                    'ppe': ppe,
                    'n95_masks': n95,
                    'reusable_masks': reusablemask,
                    'disposable_masks': disposablemask,
                    'gloves': gloves,
                    'sanitizer': sanitizer
                }
            except:
                pass
            else:
                result.append(tmp)
            
        return result

    def extract_vaccination_info(self, tables):

        vax_table = None
        keywords = {'vaccination', 'first', 'second', 'dose'}
        vax_table = common_utils.find_table_by_keywords(tables, keywords)

        if vax_table is None:
            return None
        
        # Extract information from relevant columns
        df_dict = common_utils.convert_df_to_dict(vax_table, key_idx=1, val_idx=2)
        keymap = {
            'total_vax_today': ['total', 'people', 'vaccinated'],
            'first_dose_today': ['first dose on'],
            'second_dose_today': ['second dose on'],
            'cumulative_vax': ['cumulative', 'vaccination', 'till'],
            'cumulative_vax_first_dose': ['cumulative', 'vaccination', 'first', 'dose'],
            'cumulative_vax_sec_dose': ['cumulative', 'vaccination', 'second', 'dose'],
            'cvc_count': ['vaccination', 'center', 'cvc'],
            'aefi_cases': ['aefi', 'cases'],
            'vax_wastage': ['vaccine', 'wastage']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        if 'vax_wastage' in result:
            result['vax_wastage'] = float(common_utils.clean_numbers_str(result['vax_wastage']))

        for k in keymap.keys():
            if k in result and k not in ['vax_wastage']:
                result[k] = locale.atoi(result[k])
            
        return result

    def extract_counselling_info(self, tables):

        counselling_table = None
        keywords = {'consultations', 'ambulance', 'counselling', 'queries'}
        counselling_table = common_utils.find_table_by_keywords(tables, keywords)

        if counselling_table is None:
            return None
        
        # Extract information from relevant columns
        n = counselling_table.shape[1]
        df_dict = common_utils.convert_df_to_dict(counselling_table, key_idx=n-2, val_idx=n-1)
        
        keymap = {
            'general_queries_24h': ['queries', '24', 'hour', 'addressed'],
            'general_queries_cum': ['queries', 'addressed', 'till'],
            'consultations_24h': ['consultations', '24', 'hour'],
            'consultations_total': ['consultations', 'total', 'till'],
            'ambulances_assigned_24h': ['ambulance', '24', 'hour', 'assign'],
            'ambulances_calls_24h': ['call', 'receive', '24', 'hour'],
            'telepsych_counselling_24h': ['counselling', '24', 'hour'],
            'telepsych_counselling_total': ['counselling', 'till', 'given']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        for k in result.keys():
            result[k] = locale.atoi(result[k])

        result['date'] = self.date
            
        return result

    def extract(self):
        
        n = common_utils.n_pages_in_pdf(self.report_fpath)
        all_tables = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        tables_page0 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[1])
        tables_page1 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[2])
        tables_page0_tabula = common_utils.get_tables_from_pdf(library='tabula', pdf_fpath=self.report_fpath, pages=[1])
        tables_pagen = common_utils.get_tables_from_pdf(library='tabula', pdf_fpath=self.report_fpath, pages=[n])

        case_info = self.extract_case_info(tables_page0)
        hospital_info = self.extract_hospital_and_quarantine_info(tables_page0_tabula, tables_page0)
        testing_info = self.extract_testing_info(tables_page0)
        districtwise_info = self.extract_district_wise_info(tables_page1)
        testing_labs_info = self.extract_testing_lab_info(all_tables)
        ppe_info = self.extract_ppe_info(all_tables)
        vax_info = self.extract_vaccination_info(tables_page0)
        counselling_info = self.extract_counselling_info(tables_pagen)
        
        result = {
            'case-info': case_info,
            'hospital': hospital_info,
            'testing': testing_info,
            'district-cases': districtwise_info,
            'testing-labs': testing_labs_info,
            'ppe-info': ppe_info,
            'vax-info': vax_info,
            'counselling-info': counselling_info
        }

        return result
        
if __name__ == '__main__':
    date = '01-may-2021'
    path = "../../localstore/bulletins/WB/WB-Bulletin-2021-6-25.pdf"
    obj = WestBengalExtractor(date, path)
    print(obj.extract())