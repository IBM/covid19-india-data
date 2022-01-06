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


class DelhiExtractor(object):
    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

    def extract_testing_info(self, tables):

        def is_testing_table(df):
            keywords = {'rtpcr', 'rapid', 'antigen'}
            found = set()
            col0 = list(df[0])

            for text in col0:
                for key in keywords:
                    if key in text.lower():
                        found.add(key)
            
            if len(keywords) == len(found):
                return True
            return False

        keywords = {
            'rtpcr_test_24h': ['rtpcr', 'test'],
            'antigen_test_24h': ['rapid', 'antigen', 'test'],
            'total_tests': ['total', 'tests'],
            'tests_per_million': ['tests', 'million']
        }
        result = {}
        result['date'] = self.date

        testing_table = None
        for table in tables:
            if is_testing_table(table.df):
                testing_table = table.df
                break
        
        if testing_table is None:
            return None
        
        for _, row in testing_table.iterrows():
            text, val = row[0], row[1]

            for id, keys in keywords.items():
                if False in [key in text.lower() for key in keys]:
                    continue
                    
                result[id] = val
        
        return result


    def extract_vaccination_info(self, tables):

        def is_vaccination_table(df):
            keywords = {'beneficiaries', 'vaccinated'}
            found = set()
            col0 = list(df[0])

            for text in col0:
                for key in keywords:
                    if key in text.lower():
                        found.add(key)
            
            if len(keywords) == len(found):
                return True
            return False

        if self.date >= "2022-01-04":
            order = ['vax_total_24h', 'vax_first_dose_24h', 'vax_sec_dose_24h', None, 'vax_cumulative', 'vax_cumulative_first_dose', 'vax_cumulative_sec_dose']
        else:
            order = ['vax_total_24h', 'vax_first_dose_24h', 'vax_sec_dose_24h', 'vax_cumulative', 'vax_cumulative_first_dose', 'vax_cumulative_sec_dose']
        result = {}
        result['date'] = self.date

        vax_table = None
        for table in tables:
            if is_vaccination_table(table.df):
                vax_table = table.df
                break
        
        if vax_table is None:
            return None

        for i, row in vax_table.iterrows():
            if order[i] is None:
                continue
            val = common_utils.clean_numbers_str(row[1])
            result[order[i]] = int(val.strip())
        
        return result

    
    def extract_hospital_info(self, tables):

        def is_hospital_table(df):
            keywords = {'hospital', 'covid', 'health', 'home', 'isolation'}
            found = set()
            col0 = list(df[0])

            for text in col0:
                for key in keywords:
                    if key in text.lower():
                        found.add(key)
            
            if len(keywords) == len(found):
                return True
            return False

        order = ['hospital_beds', 'covid_care_center_beds', 'covid_health_center_beds', 'home_isolation_count']
        result = {}
        result['date'] = self.date

        hospital_table = None
        for table in tables:
            if is_hospital_table(table.df):
                hospital_table = table.df
                break
        
        if hospital_table is None:
            return None

        for i, row in hospital_table.iterrows():
            
            # Skip header row
            if i == 0:
                continue

            if order[i-1] == 'home_isolation_count':
                val = row[1].strip()
                if val.isdigit():
                    result[order[i-1]] = int(val)

            elif hospital_table.shape == (5, 4):
                try:
                    result[order[i-1] + '_total'] = int(common_utils.clean_numbers_str(row[1]))
                except:
                    pass

                try:
                    result[order[i-1] + '_occupied'] = int(common_utils.clean_numbers_str(row[2]))
                except:
                    pass

                try:
                    result[order[i-1] + '_vacant'] = int(common_utils.clean_numbers_str(row[3]))
                except:
                    pass
            
            else:
                vals = [x for x in row[1].split(' ') if x.strip().isdigit()]
                
                if len(vals) == 3:
                    result[order[i-1] + '_total'] = int(common_utils.clean_numbers_str(vals[0]))
                    result[order[i-1] + '_occupied'] = int(common_utils.clean_numbers_str(vals[1]))
                    result[order[i-1] + '_vacant'] = int(common_utils.clean_numbers_str(vals[2])) 
                
        
        return result

    
    def extract_containment_info(self):

        def is_containment_table(text):
            keywords = {'containment zones', 'ambulance', 'calls'}
            found = set()

            for key in keywords:
                if key in text.lower():
                    found.add(key)
            
            return len(keywords) == len(found)

        containment_text = None
        for page_layout in extract_pages(self.report_fpath):
            for element in page_layout:
                if isinstance(element, pdfminer.layout.LTTextBoxHorizontal):
                    text = element.get_text()
                    if is_containment_table(text):
                        containment_text = text
                        break
        
        if containment_text is None:
            return None

        containment_text = [x.strip().lower() for x in containment_text.split('\n') if len(x.strip()) > 0]
        result = {'date': self.date}
        keywords = {
            'containment_zones': ['containment zone'],
            'calls_covid_helpline': ['control room', 'covid helpline'],
            'calls_ambulance_total' : ['ambulance'], 
            'calls_refused': ['calls refused']
        }

        for key, vals in keywords.items():
            for text in containment_text:
                for val in vals:
                    if val in text:
                        keyval = text.split(':')[1].strip()

                        try:
                            result[key] = int(keyval)
                        except:
                            result[key] = 0
                        
                        break

        return result


    def extract_case_info(self, tables):
        
        def is_case_today_table(df):
            keywords = {'positive', 'recovered', 'discharged', 'death'}
            found = set()
            col0 = list(df[0])

            for text in col0:
                for key in keywords:
                    if key in text.lower():
                        found.add(key)
            
            if len(keywords) == len(found):
                return True
            return False

        def is_case_cumulative_table(df):
            keywords = {'cumulative', 'positive', 'recovered', 'fatality', 'rate'}
            found = set()
            col0 = list(df[0])

            for text in col0:
                for key in keywords:
                    if key in text.lower():
                        found.add(key)
            
            if len(keywords) == len(found):
                return True
            return False


        cumulative_result = {'date': self.date}
        case_result = {'date': self.date}

        case_today_table, case_cum_table = None, None
        for table in tables:
            if is_case_cumulative_table(table.df):
                case_cum_table = table.df
            elif is_case_today_table(table.df):
                case_today_table = table.df

        if case_cum_table is not None:
            # New format
            cumulative_keywords = {
                'cumulative_positive_cases': ['cumulative', 'positive', 'case'],
                'cumulative_positivity_rate': ['cumulative', 'positivity', 'rate'],
                'cumulative_recovered': ['recovered', 'discharged'],
                'cumulative_deaths': ['death'],
                'cumulative_cfr': ['fatality', 'rate'],
                'active_cases': ['active', 'case']
            }

            for key, vals in cumulative_keywords.items():
                for i, row in case_cum_table.iterrows():
                    if False not in [val in row[0].lower() for val in vals]:
                        try:
                            v = common_utils.clean_numbers_str(row[1])
                            cumulative_result[key] = float(v)
                        except:
                            cumulative_result[key] = 0

            
            case_keywords = {
                'cases_positive': ['positive', 'case'],
                'tests_conducted': ['test', 'conducted'],
                'positivity_rate': ['positivity', 'rate'],
                'cases_recovered': ['recovered', 'discharged'],
                'deaths': ['deaths']
            }

            for key, vals in case_keywords.items():
                for i, row in case_today_table.iterrows():
                    if False not in [val in row[0].lower() for val in vals]:
                        try:
                            v = common_utils.clean_numbers_str(row[1])
                            case_result[key] = float(v)
                        except:
                            case_result[key] = 0

        elif case_cum_table is None and case_today_table is not None and case_today_table.shape[1] >= 3:
            # Old format
            case_keywords = {
                'cases_positive': ['positive', 'case'],
                'cases_recovered': ['recovered', 'discharged'],
                'deaths': ['death'],
                'active_cases': ['active', 'case']
            }

            for key, vals in case_keywords.items():
                for i, row in case_today_table.iterrows():
                    if False not in [val in row[0].lower() for val in vals]:
                        
                        if key == 'cases_positive':
                            case_result[key] = int(common_utils.clean_numbers_str(row[1]))
                            cumulative_result['cumulative_positive'] = int(common_utils.clean_numbers_str(row[2]))
                        elif key == 'cases_recovered':
                            case_result[key] = int(common_utils.clean_numbers_str(row[1]))
                            cumulative_result['cumulative_recovered'] = int(common_utils.clean_numbers_str(row[2]))
                        elif key == 'deaths':
                            case_result[key] = int(common_utils.clean_numbers_str(row[1]))
                            cumulative_result['cumulative_deaths'] = int(common_utils.clean_numbers_str(row[2]))
                        elif key == 'active_cases':
                            if row[1].strip().isdigit():
                                cumulative_result['active_cases'] = int(common_utils.clean_numbers_str(row[1]))
                            elif row[2].strip().isdigit():
                                cumulative_result['active_cases'] = int(common_utils.clean_numbers_str(row[2]))
            
        return case_result, cumulative_result


    def extract_moderate_severe_patient_nums(self, tables):

        keywords = {'asymptomatic', 'moderate', 'severe', 'patient', 'hospital'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None
        
        df_dict = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=1)
        keymap = {
            'patients_in_hospital': ['patient', 'admit', 'hospital'],
            'asymptomatic_patients': ['mild', 'asymptomatic', 'patient'],
            'moderate_patients': ['moderate', 'patient'],
            'severe_patients': ['severe', 'patient']
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        for k in result.keys():
            result[k] = locale.atoi(result[k])
        result['date'] = self.date
        return result


    def extract(self):
        tables = common_utils.get_tables_from_pdf('camelot', self.report_fpath)
        # tables = camelot.read_pdf(self.report_fpath, strip_text='"\n')

        test_result = self.extract_testing_info(tables)
        vax_result = self.extract_vaccination_info(tables)
        hospital_result = self.extract_hospital_info(tables)
        containment_result = self.extract_containment_info()
        case_info_today, case_info_cumulative = self.extract_case_info(tables)
        moderate_severe_patients_info = self.extract_moderate_severe_patient_nums(tables)

        result = {
            'testing_vals': test_result,
            'vaccination_vals': vax_result,
            'hospital_vals': hospital_result,
            'containment_vals': containment_result,
            'case_info_vals': case_info_today,
            'cumulative_case_info': case_info_cumulative,
            'hospitalizations_info': moderate_severe_patients_info
        }
        
        return result


if __name__ == '__main__':
    date = '2022-01-04'
    path = "../../localstore/bulletins/delhi/Delhi-Bulletin-2020-8-18.pdf"
    obj = DelhiExtractor(date, path)
    print(obj.extract())