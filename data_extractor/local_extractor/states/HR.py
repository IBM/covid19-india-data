import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pandas as pd

try:
    from local_extractor.states.state_utils import HR_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor', 'states')
    if path not in sys.path:
        sys.path.insert(0, path)
    from state_utils import HR_utils

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class HaryanaExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath


    def _get_all_nums_(self, text):
        regex = re.compile(r'(\d+)')
        m = regex.findall(text)
        nums = [x for x in m]
        return nums


    def _process_column_(self, datadict, colname, new_cols, del_old):

        if colname not in datadict:
            return datadict
        
        nums = self._get_all_nums_(datadict[colname])

        n = min(len(nums), len(new_cols))

        for i in range(n):
            datadict[new_cols[i]] = nums[i]

        if del_old:
            del datadict[colname]
        
        return datadict

    
    def _process_vax_column_(self, datadict, colname, new_cols, del_old):

        if colname not in datadict:
            return datadict
        
        val = datadict[colname]
        val = val.replace('1st', '').replace('2nd', '')
        nums = self._get_all_nums_(val)

        if len(nums) != len(new_cols):
            datadict[new_cols[0]] = nums[0]
        else:
            for i, col in enumerate(new_cols):
                datadict[col] = nums[i]

        if del_old:
            del datadict[colname]

        return datadict


    def extract_caseinfo(self):

        tables_page1 = common_utils.get_tables_from_pdf(
            library='camelot', pdf_fpath=self.report_fpath, pages=[1], split_text=False
        )

        if len(tables_page1) == 0:
            return None

        table = tables_page1[0].df

        df_dict = common_utils.convert_df_to_dict(table, key_idx=0, val_idx=1)
        keymap = {
            'samples_taken_today': ['sample', 'taken', 'today'],
            'samples_sent_cumulative': ['sample', 'sent', 'till', 'date'],
            'samples_negative_cumulative': ['sample', 'found', 'negative'],
            'samples_positive_cumulative': ['sample', 'found', 'positive'],
            'samples_result_awaited': ['sample', 'result', 'awaited'],
            'cases_new': ['positive', 'case', 'today'],
            'people_put_on_surveillance_cumulative': ['person', 'cumulative', 'surveillance'],
            'people_completed_surveillance_cumulative': ['person', 'complete', 'surveillance'],
            'people_currently_under_surveillance': ['person', 'current', 'surveillance'],
            'people_home_isolation': ['home', 'isolation'],
            'recoveries_cumulative': ['total', 'patient', 'recover', 'discharge'],
            'active_cases': ['active', 'patient'],
            'deaths': ['deaths'],
            'vax_today': ['people', 'vaccinat', 'today'],        
            'vax_cumulative': ['cumulative', 'vaccination', 'coverage'],
            'positivity_rate_today': ['today', 'positi', 'rate'],
            'positivity_rate_cumulative': ['cumulative', 'positiv', 'rate'],
            'recovery_rate': ['recovery', 'rate'],
            'fatality_rate': ['fatality', 'rate'],
            'tests_per_million': ['test', 'million']
        }
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # Process `samples_positive_cumulative`
        result = self._process_column_(
            result, 'samples_positive_cumulative', 
            [
                'samples_positive_cumulative_total', 
                'samples_positive_cumulative_male', 
                'samples_positive_cumulative_female',
                'samples_positive_cumulative_transgender'
            ],
            del_old=True
        )

        result = self._process_column_(
            result, 'deaths',
            ['deaths_total', 'deaths_male', 'deaths_female', 'deaths_transgender'],
            del_old=True
        )

        result['fatality_rate'] = common_utils.clean_numbers_str(result.get('fatality_rate', None))
        result['recovery_rate'] = common_utils.clean_numbers_str(result.get('recovery_rate', None))

        result = self._process_vax_column_(
            result, 'vax_today', [
                'vax_today_total', 'vax_today_first_dose', 'vax_today_second_dose'
            ], del_old=True
        )

        for key, val in result.items():
            if key == 'date':
                continue

            try:
                val = common_utils.clean_numbers_str(val)
            except:
                pass

            try:
                result[key] = locale.atoi(val)
            except Exception:
                result[key] = locale.atof(val)


        return result


    def extract_district_info(self):

        tables_page2 = common_utils.get_tables_from_pdf(
            library='camelot', pdf_fpath=self.report_fpath, pages=[2], split_text=False
        )

        if len(tables_page2) == 0:
            return None

        table = tables_page2[0].df
        datadict = HR_utils.convert_district_table_to_dict(table)
        datalist = HR_utils.process_district_data(datadict)

        for datadict in datalist:
            datadict = self._process_column_(
                datadict, 'recovered_total', ['recovered_total', 'recovered_new'], False
            )
            datadict = self._process_column_(
                datadict, 'deaths_total', ['deaths_total', 'deaths_new'], False
            )

            datadict['date'] = self.date

            # Convert values to int
            for key, val in datadict.items():

                if key in ['date', 'district_name']:
                    continue
                    
                try:
                    val = common_utils.clean_numbers_str(val)
                except:
                    pass

                try:
                    datadict[key] = locale.atoi(val)
                except Exception:
                    datadict[key] = locale.atof(val)
         
        return datalist


    def extract_critical_case_info(self):

        npages = common_utils.n_pages_in_pdf(self.report_fpath)
        keywords = {'oxygen', 'support', 'patient'}
        
        for pageno in range(3, npages + 1):
            pagetables = common_utils.get_tables_from_pdf(
                library='camelot', pdf_fpath=self.report_fpath, pages=[pageno], split_text=False
            )

            datatable = common_utils.find_table_by_keywords(pagetables, keywords)
            if datatable is None:
                continue
            else:
                # table found. Try to find the remaining part of the table
                next_pageno = pageno + 1
                if next_pageno > npages:
                    break

                nextpage_tables = common_utils.get_tables_from_pdf(
                    library='camelot', pdf_fpath=self.report_fpath, pages=[next_pageno], split_text=False
                )

                if len(nextpage_tables) == 0:
                    break

                nextpage_table = nextpage_tables[0].df

                if nextpage_table.shape[1] == datatable.shape[1]:
                    datatable = pd.concat([datatable, nextpage_table])
                    break

        if datatable is None:
            return None

        datalist = HR_utils.process_critical_covid_info(datatable)

        for row in datalist:
            row['date'] = self.date
            row['facility_name'] = common_utils.clean_numbers_str(row['facility_name']).lower()

        return datalist

    def extract(self):

        caseinfo = self.extract_caseinfo()
        districtinfo = self.extract_district_info()
        criticalcaseinfo = self.extract_critical_case_info()

        result = {
            'case-information': caseinfo,
            'district-information': districtinfo,
            'critical-case-information': criticalcaseinfo
        }

        return result


if __name__ == '__main__':

    date = '2021-01-01'
    # path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/HR/HR-Bulletin-2021-10-01.pdf"
    # path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/HR/HR-Bulletin-2021-04-20.pdf"
    path = "/Users/mayank/Documents/projects/opensource/covid19-india-data/localstore/bulletins/HR/HR-Bulletin-2020-07-20.pdf"

    obj = HaryanaExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())