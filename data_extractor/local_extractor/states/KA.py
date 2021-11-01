import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pandas as pd
import camelot
import pdfminer

from pdfminer.high_level import extract_pages
from pprint import pprint

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils

class KarnatakaExtractor(object):
    def __init__(self, date, report_fpath):
        super().__init__()
        self.date = date
        self.report_fpath = report_fpath

    def _get_term_and_value(self, series):
        term_before_value = {
            'Today’s Discharges': 'discharged_new',
            'Total Discharges': 'discharged_total',
            'New Cases Reported': 'cases_new',
            'Total Active Cases': 'cases_active_new',
            'New Covid Deaths': 'deaths_new',
            'Total Covid Deaths': 'deaths_total',
            'Total Positive Cases': 'cases_active_total',
            'Positivity rate for the day': 'positivity_rate_percent',
            'Case fatality rate': 'fatality_rate_percent'
        }
        detected_term = None
        detected_value = None
        for it in series:
            for k, v in term_before_value.items():
                if (re.search(k, it, re.IGNORECASE)):
                    detected_term = v
                raw_string = it.strip()
                if raw_string.isdigit():
                    detected_value = int(raw_string)
                elif '%' in raw_string:
                    try:
                        detected_value = float(raw_string[:-1])
                    except:
                        pass
        if detected_term is not None and detected_value is not None:
            return (detected_term, detected_value)
        return (None, None)

    def extract_case_info(self, table):
        if table is None:
            return None
        df_dict = {}
        for i, row in table.df.iterrows():
            term, value = self._get_term_and_value(row.values)
            if term is not None:
                df_dict[term] = value
        df_dict['date'] = self.date

        return df_dict

    def extract_district_case_information(self, table):
        if table is None:
            return None
        d = table.df
        # The first 2 rows are blank. The third row is the table title. The fourth row
        # has the column headers. The last two rows have the totals and some footnote.
        d = d.iloc[4:(len(d)-2)]
        result = []
        for i, row in d.iterrows():
            tmp = {
                'date': self.date,
                'district': row[2],
                'cases_new': row[3],
                'cases_total': row[4],
                'discharged_new': row[5],
                'discharged_total': row[6],
                'active_cases_total': row[7],
                'deaths_new': row[8],
                'deaths_total': row[9],
                'non_covid_deaths': row[10]
            }
            result.append(tmp)
        return result

    def extract(self):
        n = common_utils.n_pages_in_pdf(self.report_fpath)

        # karnataka has one table per page, and each table inside it has 
        # a complex system of text and tables embedded in it.

        # First, we get the overall case numbers from the first page.
        # This has to be done without smart boundary detection.
        tables_page0 = common_utils.get_tables_from_pdf(library='camelot', 
            pdf_fpath=self.report_fpath, 
            smart_boundary_detection=False,
            pages=[1])
        case_info = self.extract_case_info(tables_page0[0])

        # Then, we get the district-wise numbers. This needs smart boundary detection.
        tables_page4 = common_utils.get_tables_from_pdf(library='camelot', 
            pdf_fpath=self.report_fpath, 
            smart_boundary_detection=True,
            pages=[4])
        districtwise_info = self.extract_district_case_information(tables_page4[1])

        result = {
            'case_info': case_info,
            'district-cases': districtwise_info
        }

        return result



if __name__ == '__main__':
    date = '08-oct-2021'
    path = '/home/sushovan/covdata/bulletins/KA/KA-Bulletin-2021-10-28.pdf'
    obj = KarnatakaExtractor(date, path)
    print(obj.extract())