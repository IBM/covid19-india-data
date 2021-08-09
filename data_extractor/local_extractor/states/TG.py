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


class TelanganaExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        self.nums_regex = re.compile(r'([\d\.,]+)')

    def _process_case_nums_(self, datadict, colname, new_cols, del_old=False):

        if colname in datadict:
            m = self.nums_regex.findall(datadict[colname])
            
            if len(m) == 1:
                datadict[new_cols[0]] = None
                datadict[new_cols[1]] = m[0]
            elif len(m) == 2:
                datadict[new_cols[0]] = m[0]
                datadict[new_cols[1]] = m[1]

        if del_old and colname in datadict:
            del datadict[colname]

        return datadict


    def extract_symptomatic_asymptomatic_info(self, tables):

        datatable = None
        keywords = {'total', 'symptomatic', 'asymptomatic'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None
        
        df_dict = common_utils.convert_df_to_dict(datatable, key_idx=1, val_idx=-1)
        keymap = {
            'total_positives': ['total', 'positives'],
            'asymptomatic': ['asymptomatic'],
            'symptomatic': [' symptomatic']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # clean result
        result = self._process_case_nums_(result, 'asymptomatic', ['total_asymptomatic', 'perc_asymptomatic'], del_old=True)
        result = self._process_case_nums_(result, 'symptomatic', ['total_symptomatic', 'perc_symptomatic'], del_old=True)
        
        for k, v in result.items():
            if k == 'date' or v is None:
                continue
            elif k.startswith('perc_'):
                result[k] = locale.atof(v)
            else:
                result[k] = locale.atoi(v)

        return result

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

    def extract_age_wise_info(self, tables):

        datatable = None
        keywords = {'age', 'wise', 'positive', 'male', 'female'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        datatable = datatable.iloc[-10:]
        colorder = [
            'ages_upto_10', 'ages_11_to_20', 'ages_21_to_30', 'ages_31_to_40', 'ages_41_to_50',
            'ages_51_to_60', 'ages_61_to_70', 'ages_71_to_80', 'ages_81_and_above', 'total'
        ]
        subcolorder = ['total', 'male', 'female']
        result = {
            'date': self.date
        }

        i = 0
        for _, row in datatable.iterrows():
            n = len(row)
            data = row[:n-1].tolist()
            data.extend(str(row[-1]).strip().split(' '))

            result[colorder[i] + '_' + subcolorder[0]] = locale.atof(str(data[-3]).strip())
            result[colorder[i] + '_' + subcolorder[1]] = locale.atof(str(data[-2]).strip())
            result[colorder[i] + '_' + subcolorder[2]] = locale.atof(str(data[-1]).strip())

            i += 1

        return result
            

    def extract(self):

        all_tables_tabula = common_utils.get_tables_from_pdf(library='tabula', pdf_fpath=self.report_fpath)

        symptomatic_info = self.extract_symptomatic_asymptomatic_info(all_tables_tabula)
        comorbities_info = self.extract_comorbidities_fatality_info(all_tables_tabula)
        agewise_info = self.extract_age_wise_info(all_tables_tabula)

        result = {
            'asymptomatic-status': symptomatic_info,
            'comorbidities-fatality': comorbities_info,
            'agewise-info': agewise_info
        }

        return result

    
if __name__ == '__main__':
    date = '01-may-2021'
    path = "../../localstore/bulletins/TG/TG-Bulletin-2021-7-14.pdf"
    obj = TelanganaExtractor(date, path)
    
    from pprint import pprint
    pprint(obj.extract())