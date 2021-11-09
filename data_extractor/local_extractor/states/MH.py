import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pdfplumber
import pandas as pd
import dateparser


try:
    from local_extractor.utils import common_utils
    from local_extractor.utils import custom_exceptions
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils
    from utils import custom_exceptions


class MaharashtraExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

    
    def __day_suffix__(self, day):
        
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]
        
        return suffix


    def __verify_bulletin_correct_date__(self):

        text_page0 = self.__get_text__(0)
        datestr = '{}{}[ ]+{}[ ]+{}'
        date = dateparser.parse(self.date)

        day = date.day
        suffix = self.__day_suffix__(day)
        month = date.strftime('%B').lower()
        year = date.year

        re_str = datestr.format(day, suffix, month, year)
        regex = re.compile(re_str, re.IGNORECASE)
        match = regex.search(text_page0)

        if match:
            return True
        return False

    def __get_text__(self, page):

        with pdfplumber.open(self.report_fpath) as pdf:
            first_page = pdf.pages[page]
            text = first_page.extract_text()
        return text

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

    def get_regex_match(self, text, regex):

        vals = regex.findall(text)
        if vals:
            val = vals[0]
            text = regex.sub('', text, 1)
            return text, val
        
        return text, None


    def get_case_info(self):

        cols = [
            ('discharged_today', re.compile(r'([\d,]+)[ ]+patients[ ]+discharged[ ]+today', re.IGNORECASE)),
            ('discharged_total', re.compile(r'([\d,]+)[ ]+[ ]+patients[ ]+discharged', re.IGNORECASE)),
            ('recovery_rate', re.compile(r'recovery[ ]+rate\D+([\d\.,]+)', re.IGNORECASE)),
            ('cases_new', re.compile(r'([\d,]+) new cases', re.IGNORECASE)),
            ('deaths_new', re.compile(r'([\d,]+)\D+deaths', re.IGNORECASE)),
            ('cfr', re.compile(r'case fatality rate\D+([\d\.,]+)', re.IGNORECASE)),
            ('tests_cumulative', re.compile(r'([\d,]+)[ ]+laboratory[ ]+samples', re.IGNORECASE)),
            ('tests_positive_cumulative', re.compile(r'([\d,]+)\D+tested[ ]+positive', re.IGNORECASE)),
            ('current_home_quarantine', re.compile(r'([\d,]+)\D+home[ ]+quarantine', re.IGNORECASE)),
            ('current_institutional_quarantine', re.compile(r'([\d,]+)\D+institutional[ ]+quarantine', re.IGNORECASE)),
            ('active_cases', re.compile(r'([\d,]+)[ ]+active[ ]+cases', re.IGNORECASE))
        ]

        page0_text = self.__get_text__(0)
        lines = page0_text.split('\n')

        filteredlines = []
        keepline = False

        for line in lines:
            if 'at a glance' in line.lower():
                keepline = True
                continue

            if 'sr. no.' in line.lower():
                keepline = False
                break

            if keepline:
                filteredlines.append(line)

        text = ' '.join(filteredlines).lower()
        text = text.replace('covid-19', '')

        data = {}
        for colname, colregex in cols:

            text, val = self.get_regex_match(text, colregex)

            if val is None:
                continue

            try:
                val = locale.atoi(val)
            except Exception:
                val = locale.atof(val)

            data[colname] = val

        data['date'] = self.date

        return data

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

        if not self.__verify_bulletin_correct_date__():
            raise custom_exceptions.UnprocessedBulletinException('Bulletin failed to match current date')

        all_tables = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        all_tables = self.join_tables(all_tables)

        case_info = self.get_case_info()
        active_case_info = self.extract_citycase_info(all_tables)
        district_case_info = self.extract_district_level_info(all_tables)

        result = {
            'case-info': case_info,
            'active-case-info': active_case_info,
            'district-case-info': district_case_info
        }

        return result


if __name__ == '__main__':

    date = '2021-01-01'
    path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/MH/MH-Bulletin-2021-10-30.pdf"

    obj = MaharashtraExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())