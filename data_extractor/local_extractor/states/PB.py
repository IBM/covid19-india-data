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


class PunjabExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        # for matching 3(Amritsar-1, Ludhiana-2)
        self.district_regex = re.compile(r'([\d]+)\(([\d,\D,\s]+)\)')

    def _process_district_info_(self, data, col, new_cols, del_old=False):
        if col in data:
            m = self.district_regex.match(data[col])
            if m:
                parsed = m.groups()
                data[new_cols[0]] = parsed[0]
                data[new_cols[1]] = parsed[1]

            if del_old:
                del data[col]

            return data

    def extract_cases_info(self, tables):
        info_table = None
        keywords = {'samples', 'vaccination', 'conducted', 'discharged'}

        info_table = common_utils.find_table_by_keywords(tabels, keywords)

        if info_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(info_table, key_idx=1, val_idx=2)
        keymap = {
            'samples_total': ['total', 'samples', 'taken'],
            'samples_new': ['sample', 'collected', 'day'],
            'tests_new': ['test', 'conducted', 'day'],
            'cases_total': ['patiens', 'tested', 'positive'],
            'discharged_total': ['patients', 'discharged'],
            'active_cases': ['number', 'active', 'cases'],
            'deaths_total': ['total', 'deaths', 'reported'],
            'oxygen_support_active_patients': ['patients', 'oxygen', 'support'],
            'critical_care_active_patients': ['critical', 'care', 'level-3', 'facilities'],
            'ventilator_support_active_patients': ['critical', 'ventilator', 'support'],
            'healthcare_first_vaccination_today': ['healthcare', 'vaccinated', '1st', 'dose', 'day'],
            'healthcare_first_vaccination_total': ['total', 'healthcare', 'vaccinated', '1st', 'dose'],
            'frontline_first_vaccination_today': ['frontline', 'vaccinated', '1st', 'dose', 'day'],
            'frontline_first_vaccination_total': ['total', 'frontline', 'vaccinated', '1st', 'dose'],
            'healthcare_second_vaccination_today': ['healthcare', 'vaccinated', '2nd', 'dose', 'day'],
            'healthcare_second_vaccination_total': ['total', 'healthcare', 'vaccinated', '2nd', 'dose'],
            'frontline_second_vaccination_today': ['frontline', 'vaccinated', '2nd', 'dose', 'day'],
            'frontline_second_vaccination_total': ['total', 'frontline', 'vaccinated', '2nd', 'dose'],
            'above_45_first_vaccination_today': ['above', '45', 'vaccinated', '1st', 'dose', 'day'],
            'above_45_first_vaccination_total': ['total', 'above', '45', 'vaccinated', '1st', 'dose'],
            'above_45_second_vaccination_today': ['above', '45', 'vaccinated', '2nd', 'dose', 'day'],
            'above_45_second_vaccination_total': ['total', 'above', '45', 'vaccinated', '2nd', 'dose'],
            'eighteen_44_first_vaccination_today': ['18-44', 'vaccinated', '1st', 'dose', 'day'],
            'eighteen_44_first_vaccination_total': ['total', '18-44', 'vaccinated', '1st', 'dose'],
            'eighteen_44_second_vaccination_today': ['18-44', 'vaccinated', '2nd', 'dose', 'day'],
            'eighteen_44_second_vaccination_total': ['total', '18-44', 'vaccinated', '2nd', 'dose'],
            'first_vaccination_today': ['total', '1st', 'vaccination', 'dose', 'day'],
            'second_vaccination_today': ['total', '2nd', 'vaccination', 'dose', 'day'],
            'total_vaccination_today': ['total', '1st', 'and', '2nd', 'vaccination', 'dose', 'day']
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        # clean result
        for col in result.keys():
            if "*" in result[col]:
                result[col] = result[col].replace("*", "")

            result[col] = locale.atoi(result[col])

        result["date"] = self.date

        return result

    def extract_patient_info(self, tables):
        info_table = None
        keywords = {"icu", "ventilator", "discharged", "deaths"}

        info_table = common_utils.find_table_by_keywords(tabels, keywords)

        if info_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(info_table, key_idx=1, val_idx=2)

        keymap = {
            'icu_patients_today': ["admitted", "icu"],
            'ventilator_patients_today': ["put", "ventilator", "support"],
            'discharged_patients_today': ["patients", "discharged"],
            'deaths_today': ["deaths", "reported"]
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        # clean up the data
        result = self._process_district_info_(result, 'icu_patients_today', ["icu_patients_today", "icu_patients_today_districts"])
        result = self._process_district_info_(result, 'ventilator_patients_today', ["ventilator_patients_today", "ventilator_patients_today_districts"])
        result = self._process_district_info_(result, 'discharged_patients_today', ["discharged_patients_today", "discharged_patients_today_districts"])
        result = self._process_district_info_(result, 'death_today', ["deaths_today", "deaths_today_districts"])

        for col in keymap.keys():
            result[col] = locale.atoi(result[col])

        result["date"] = self.date

        return result



    def extract(self):
        n = common_utils.n_pages_in_pdf(self.report_fpath)
        tables_page1 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages[1])
        tables_page2 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages[2])

        case_vaccination_info = self.extract_cases_info(tables_page1)
        is_page2_parsed = True
        if len(tables_page1) > 1:
            # this means second table with patient info is on the same page
            table_patients = tables_page1
            is_page2_parsed = False
        else:
            table_patients = tables_page2

        patients_info = self.extract_patient_info(tables_patients)


        result = {
            'cases_vaccination_details': case_vaccination_info,
            'patient_details': patients_info
        }

        return result
        
if __name__ == '__main__':
    date = '25-jul-2021'
    path = "../../downloads/bulletins/PB/Media Bulletin COVID-19_ 25-July-2021.pdf"
    obj = PunjabExtractor(date, path)
    print(obj.extract())
