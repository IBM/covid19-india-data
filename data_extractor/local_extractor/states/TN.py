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

class TamilNaduExtractor(object):
    def __init__(self, date, report_fpath):
        self.date = date
        self.report_fpath = report_fpath

        # for matching facilities string -- example 269 (69 Govt+200 Private)
        self.nums_regex = re.compile(r'([\d,]+)[ ]*\(([\d,]+)[ ]*([\D]+)[ ]*([\d,]+)[ ]*([\D]+)\)')

    def _parse_facilities_num_(self, data, col, new_cols):
        parsing_successful = False
        if col in data:
            parsed = self.nums_regex.match(data[col])
            if parsed:
                grps = parsed.groups()
                for new_col in new_cols:
                    # find the relevant index dynamically
                    # what if the government facilities are written at the end
                    if "govt" in new_col:
                        for index, s in enumerate(grps):
                            if "Govt" in s:
                                data[new_col] = grps[index - 1]
                                break
                    elif "private" in new_col:
                        for index, s in enumerate(grps):
                            if "Private" in s:
                                data[new_col] = grps[index - 1]

                data[col] = grps[0]
                parsing_successful = True

        return data, parsing_successful


    def extract_case_info(self, tables):
        caseinfo_table = None
        # there is only one table in this page
        # checking just to be sure
        if len(tables) == 1:
            caseinfo_table = tables[0].df
        else:
            keywords = {'testing', 'facilities', 'active', 'tested', 'positive', 'deaths', 'discharged', 'following', 'treatment'}
            caseinfo_table = common_utils.find_table_by_keywords(tables, keywords)

        # in case no such table found
        if caseinfo_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(caseinfo_table, key_idx=1, val_idx=1)
        keymap = {
            "testing_facilities" : ["testing", "facilities"],
            "active_cases_yesterday" : ["active", "till", "yesterday"],
            "positive_tested_cases" : ["tested", "positive"],
            "discharged_patients" : ["discharged", "treatment"],
            "deaths_today" : ["deaths"],
            "active_cases_today" : ["active", "today"]
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # cleaning up numbers
        new_cols =  ["government_testing_facilities", "private_testing_facilities"] 
        result, parsing_successful = self._parse_facilities_num_(self, result, "testing_facilities", new_cols)

        atoi_cols = list(dict.keys(keymap))
        # if parsing wasnt successful, do not append the new columns
        if parsing_successful:
            atoi_cols.extend(new_cols)

        for col in atoi_cols:
            result[col] = locale.atoi(result[col])

        return result

    def extract_detailed_cases(self, tables):
        detailed_info_table = None
        if len(tables) == 1:
            detailed_info_table = tables[0].df
        else:
            keywords = {'positive', 'deaths', 'rt-pcr', 'isolation', 'transgender', 'male', 'female'}
            detailed_info_table = common_utils.find_table_by_keywords(tables, keywords)

        # in case no such table found
        if detailed_info_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(detailed_info_table, key_idx=1, val_idx=2)
        keymap = {
            "total_active_cases": ["acitve", "including", "isolation"],
            "tested_positive_today": ["persons", "tested", "positive", "tamil"],
            "returned_road_positive_today": ["passengers", "returned", "other", "states"],
            "total_new_cases_today": ["total"],
            "total_tested_positive": ["persons", "tested", "positive", "till"],
            "rt_pcr_today": ["rt-pcr", "samples"],
            "persons_tested_rt_pcr": ["persons", "rt-pcr", "tested"],
            "male_positive_tests": ["male", "transgender", "positive", "today"],
            "total_male_positive_tests": ["male", "transgender", "positive", "till"],
            "testing_facilities": ["testing", "facilities"],
            "discharged_today": ["positive", "patients", "discharged", "following", "treatment"],
            "deaths_today": ["deaths", "today", "till"]
        }

        # TODO: check the number of total_new_cases as the row has just value in the file
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # cleaning up numbers
        atoi_cols = list(dict.keys(keymap))

        # first rtcpr samples tested
        # new_cols = 

        return result


    def extract(self):
        n = common_utils.n_pages_in_pdf(self.report_fpath)
        # file consists of a table on page 1 and an advertisement :D
        tables_page1 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[1])
        tables_page2 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[2])

        # send first table to extract the cummulative case details
        cummulative_case_info = self.extract_case_info(tables_page1)
        detailed_case_info = self.extract_detailed_cases(tables_page2)

        result = {
            'cummulative-case-info': cummulative_case_info,
            'detailed_case_info': detailed_case_info
        }

        return result


if __name__ == "__main__":
    date = "01-jun-2021"
    path = "../../downloads/bulletins/TN/TN-Bulletin-2021-6-1.pdf"
    reader = TamilNaduExtractor(date, path)
    reader.extract()
