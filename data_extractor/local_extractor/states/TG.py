import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pandas as pd
import camelot

import pdfminer
from pdfminer.high_level import extract_pages

try:
    from local_extractor.states.state_utils import TG_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor', 'states')
    if path not in sys.path:
        sys.path.insert(0, path)
    from state_utils import TG_utils

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class TelanganaExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        self.nums_regex = re.compile(r'([\d\.,]+)')

    def _process_case_nums_(self, datadict, colname, new_cols, del_old=False, new_col_if_only_1=None):

        if colname in datadict:
            m = self.nums_regex.findall(datadict[colname])
            
            if len(m) == 1:
                if new_col_if_only_1 is None:
                    datadict[new_cols[0]] = None
                    datadict[new_cols[1]] = m[0]
                else:
                    datadict[new_col_if_only_1] = m[0]
            elif len(m) == 2:
                datadict[new_cols[0]] = m[0]
                datadict[new_cols[1]] = m[1]

        if del_old and colname in datadict:
            del datadict[colname]

        return datadict


    def extract_daily_case_info(self, tables):

        datatable = None
        keywords = {'positive', 'recovered', 'death', 'isolation'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None
        
        datatable = datatable.iloc[1:]
        df_dict = TG_utils.process_caseinfo_table(datatable)
        keymap = {
            'total_positives': ['positive', 'cases'],
            'total_recovered': ['recovered', 'cases'],
            'total_deaths': ['death'],
            'cfr': ['case', 'fatality', 'rate'],
            'recovery_rate': ['recovery', 'rate'],
            'cases_in_isolation': ['isolation']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # clean result
        result = self._process_case_nums_(result, 'total_positives', ['cases_new', 'cases_total'], del_old=True)
        result = self._process_case_nums_(result, 'total_recovered', ['recovered_new', 'recovered_total'], del_old=True)
        result = self._process_case_nums_(result, 'total_deaths', ['deaths_new', 'deaths_total'], del_old=True)
        result = self._process_case_nums_(result, 'cfr', ['state_CFR', 'national_CFR'], del_old=True)
        result = self._process_case_nums_(result, 'recovery_rate', ['state_recovery_rate', 'national_recovery_rate'], del_old=True)

        for k, v in result.items():
            if k == 'date' or v is None:
                continue
            if 'CFR' in k or 'recovery_rate' in k:
                result[k] = locale.atof(v)
            else:
                result[k] = locale.atoi(v)

        return result

    
    def extract_testing_info(self, tables):

        datatable = None
        keywords = {'samples', 'tested', 'report', 'awaited', 'million'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None
        
        datatable = datatable.iloc[1:]
        df_dict = TG_utils.process_testing_table(datatable)
        keymap = {
            'tests_info': ['sample', 'tested', 'today'],
            'tests_per_million': ['tested', 'million'],
            'reports_awaited': ['report', 'await']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # clean result
        result = self._process_case_nums_(result, 'tests_info', ['tests_today', 'tests_cumulative'], del_old=True)

        for k, v in result.items():
            if k == 'date' or v is None:
                continue
            result[k] = locale.atoi(v)

        return result


    def extract_contact_status_info(self, tables):

        datatable = None
        keywords = {'primary', 'secondary', 'contact'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None
        
        datatable = datatable.iloc[1:]
        df_dict = TG_utils.process_testing_table(datatable)
        keymap = {
            'testing_info': ['sample', 'tested', 'today'],
            'primary_contact_info': ['primary', 'contact'],
            'secondary_contact_info': ['secondary', 'contact']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # clean result
        result = self._process_case_nums_(result, 'testing_info', ['tests_today', 'tests_cumulative'], del_old=True, new_col_if_only_1='tests_today')
        result = self._process_case_nums_(result, 'primary_contact_info', ['primary_contacts_tested_today', 'perc_primary_contacts_tested_today'], del_old=True)
        result = self._process_case_nums_(result, 'secondary_contact_info', ['sec_contacts_tested_today', 'perc_sec_contacts_tested_today'], del_old=True)

        for k, v in result.items():
            if k == 'date' or v is None:
                continue
            if 'perc_' in k:
                result[k] = locale.atof(v)
            else:
                result[k] = locale.atoi(v)

        return result


    def extract_symptomatic_asymptomatic_info(self, tables):

        datatable = None
        keywords = {'total', 'symptomatic', 'asymptomatic'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        datatable = datatable.iloc[1:]
        df_dict = TG_utils.process_testing_table(datatable)
        keymap = {
            'total_positives': ['total', 'positives'],
            'asymptomatic': ['asymptomatic'],
            'symptomatic': [' symptomatic']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # clean result
        result = self._process_case_nums_(result, 'asymptomatic', ['total_asymptomatic', 'perc_asymptomatic'], del_old=True, new_col_if_only_1='perc_asymptomatic')
        result = self._process_case_nums_(result, 'symptomatic', ['total_symptomatic', 'perc_symptomatic'], del_old=True, new_col_if_only_1='perc_symptomatic')
        
        for k, v in result.items():
            if k == 'date' or v is None:
                continue
            elif k.startswith('perc_'):
                result[k] = locale.atof(v)
            else:
                result[k] = locale.atoi(v)

        return result
        
    """
    def extract_comorbidities_fatality_info(self, tables):

        datatable = None
        keywords = {'death', 'due', 'covid', 'comorbidities'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        n = len(datatable)
        datatable.loc[n] = datatable.columns

        df_dict = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=-1)
        keymap = {
            'perc_fatality_covid19': ['deaths', 'covid', '19'],
            'perc_fatality_comorbidities': ['deaths', 'comorbidities']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        if result.get('perc_fatality_covid19', None):
            result['perc_fatality_covid19'] = locale.atof(
                common_utils.clean_numbers_str(str(result['perc_fatality_covid19']))
            )

        if result.get('perc_fatality_comorbidities', None):
            result['perc_fatality_comorbidities'] = locale.atof(
                common_utils.clean_numbers_str(str(result['perc_fatality_comorbidities']))
            )
        
        return result
    """

    def extract_age_wise_info(self, tables):

        datatable = None
        keywords = {'age', 'wise', 'positive', 'male', 'female'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        result = TG_utils.process_agewise_table(datatable)
        return result


    def extract_district_case_information(self, tables):

        datatable = None
        keywords = {'district', 'today'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None
        
        result = TG_utils.process_district_case_table(datatable)

        for entry in result:
            entry['date'] = self.date

        return result
            

    def extract(self):

        # Bulletins prior to this date included images, which we bypass for now
        if self.date < "2020-09-01":
            return dict()

        # Only process first 4 pages of TG since that's where all the information we aim
        # to extract resides. Additionally, it saves a lot of time in unnecessarily processing
        # additional pages, which can sometime be utop 50 additional pages
        pages = list(range(4))

        all_tables_camelot_tabnet = common_utils.get_tables_from_pdf(
            library='camelot', pdf_fpath=self.report_fpath, smart_boundary_detection=True, pages=pages
        )

        # daily case information extraction
        case_info = self.extract_daily_case_info(all_tables_camelot_tabnet)

        # Testing status
        testing_info = self.extract_testing_info(all_tables_camelot_tabnet)

        # status of contacts table
        contact_testing_info = self.extract_contact_status_info(all_tables_camelot_tabnet)

        # Symptomatic vs Asymptomatic information
        symptomatic_info = self.extract_symptomatic_asymptomatic_info(all_tables_camelot_tabnet)

        # Age-wise information
        agewise_info = self.extract_age_wise_info(all_tables_camelot_tabnet)

        # District-wise information
        district_case_info = self.extract_district_case_information(all_tables_camelot_tabnet)

        # comorbities_info = self.extract_comorbidities_fatality_info(all_tables_camelot_tabnet)
        

        result = {
            'case-information': case_info,
            'testing-information': testing_info,
            'contact-testing-info': contact_testing_info,
            'asymptomatic-status': symptomatic_info,
            'agewise-info': agewise_info,
            'district-wise-info': district_case_info,
        }

        return result

    
if __name__ == '__main__':
    date = '2021-01-01'
    path = "/home/mayankag/covid19-india-data/localstore/bulletins/TG/TG-Bulletin-2021-09-23.pdf"
    # path = "/home/mayankag/covid19-india-data/localstore/bulletins/TG/TG-Bulletin-2020-09-01.pdf"
    obj = TelanganaExtractor(date, path)
    
    from pprint import pprint
    pprint(obj.extract())