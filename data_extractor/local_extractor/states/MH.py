import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pandas as pd


try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class MaharashtraExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath


    def join_tables(self, tables):
        
        ntables = len(tables)
        result = [ [] ]

        for i in range(ntables):
            
            tbl = tables[i].df
            lastrow = list(tbl.iloc[-1])
            
            # end of table found
            if 'total' in lastrow[1].lower():
                result[-1].append(tbl)
                result.append([])
            else:
                result[-1].append(tbl)

        tables_concatenated = []
        for tablelist in result:
            if len(tablelist) == 0:
                continue

            table = pd.concat(tablelist)
            tables_concatenated.append(table)

        return tables_concatenated


    def extract_citycase_info(self, tables):

        datatable = None
        keywords = {'recovered', 'active'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        datalist = []

        for _, row in datatable.iterrows():
            row = list(row)

            if 'sr' in row[0].lower() and 'no' in row[0].lower():
                continue

            district_name = row[1].lower()
            case_count = row[2]
            recoveries = row[3]
            deaths = row[4]
            deaths_other_causes = row[5]
            active_cases = row[6]

            data = {
                'date': self.date,
                'district_name': district_name,
                'cases_total': case_count,
                'recoveries_total': recoveries,
                'deaths_total': deaths,
                'deaths_total_other_causes': deaths_other_causes,
                'active_cases': active_cases
            }

            for k, v in data.items():
                if k == 'date' or k == 'district_name': 
                    continue

                try:
                    data[k] = locale.atoi(v)
                except:
                    data[k] = None

            datalist.append(data)

        return datalist


    def extract_district_level_info(self, tables):

        datatable = None
        keywords = {'prog', 'daily', 'case'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        datalist = []

        for _, row in datatable.iterrows():
            row = list(row)
            row_str = ' '.join(row).lower()

            if 'sr' in row[0].lower() and 'no' in row[0].lower():
                continue

            if 'daily' in row_str or 'prog' in row_str:
                continue

            district_name = row[1].lower()
            cases_daily = row[2]
            cases_prog = row[3]
            deaths_daily = row[4]
            deaths_prog = row[5]

            data = {
                'date': self.date,
                'district_name': district_name,
                'cases_daily': cases_daily,
                'cases_total': cases_prog,
                'deaths_daily': deaths_daily,
                'deaths_total': deaths_prog
            }

            for k, v in data.items():
                if k == 'date' or k == 'district_name': 
                    continue

                try:
                    data[k] = locale.atoi(v)
                except:
                    data[k] = None

            datalist.append(data)

        return datalist


    def extract(self):

        all_tables = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        all_tables = self.join_tables(all_tables)

        active_case_info = self.extract_citycase_info(all_tables)
        district_case_info = self.extract_district_level_info(all_tables)

        result = {
            'active-case-info': active_case_info,
            'district-case-info': district_case_info
        }

        return result


if __name__ == '__main__':

    date = '2021-01-01'
    # path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/HR/HR-Bulletin-2021-10-01.pdf"
    # path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/HR/HR-Bulletin-2021-04-20.pdf"
    path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/MH/MH-Bulletin-2021-01-02.pdf"

    obj = MaharashtraExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())