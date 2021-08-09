import re
import pandas as pd
import io

import camelot
import pdfminer
from pdfminer.high_level import extract_text, extract_pages
from pdfminer.layout import LTFigure, LTImage

from utils.table_extractor import TexTract


class Karnataka(object):
    def __init__(self, report_fpath):
        self.report_fpath = report_fpath

        self._SUMMARY_KEY = 'summary-stats'
        self._VAX_AND_TEST_KEY = 'vax-and-test-data'
        self._PROG_UPDATES_KEY = 'prog-updates'
        self._VAX_INFO_KEY = 'vax-information'
        self._DIST_COVID19_KEY = 'districtwise-covid19'
        self._TODAY_DISCHARGES_KEY = 'today-discharges'
        self._TODAY_DEATHS_KEY = 'today-deaths'
        self._ICU_KEY = 'icu-details'

        self.pagemap = self._assign_pages_()


    def _assign_pages_(self):

        npages = len(list(extract_pages(self.report_fpath)))
        page_keymap = {
            'programmatic updates': self._PROG_UPDATES_KEY,
            'vaccination program information': self._VAX_INFO_KEY,
            'districtwise abstract of covid': self._DIST_COVID19_KEY,
            'today.s discharges': self._TODAY_DISCHARGES_KEY,
            'today.s reported covid.*deaths': self._TODAY_DEATHS_KEY,
            'icu details': self._ICU_KEY
        }
        pagemap = {}

        for i in range(npages):
            
            if i == 0:
                pagemap[self._SUMMARY_KEY] = [i]
                continue
            if i == 1:
                pagemap[self._VAX_AND_TEST_KEY] = [i]
                continue
                
            pagetext = extract_text(self.report_fpath, page_numbers=[i]).replace('\n', ' ')

            for key, val in page_keymap.items():
                if re.search(key, pagetext, re.IGNORECASE):
                    if val not in pagemap:
                        pagemap[val] = []

                    pagemap[val].append(i)
        
        return pagemap


    def _str2num_(self, numstr):
        numregex = r'([\d\.]+)'
        match = re.match(numregex, numstr)
        nums = float(match.group(1))
        return nums

    def _extract_imgs_(self, pagenums):
        imgs = []

        for page_layout in extract_pages(self.report_fpath, page_numbers=pagenums):
            for element in page_layout:
                if isinstance(element, LTFigure):
                    for elem in element:
                        if isinstance(elem, LTImage):
                            imgs.append(elem)
        return imgs

    def _extract_summary_information_(self):

        KEY_IDS = [
            "(\d+)[ ]+(today.s discharges)", "(\d+)[ ]+(total discharges)", "(\d+)[ ]+(new cases reported)",
            "(\d+)[ ]+(total active cases)", "(\d+)[ ]+(new covid deaths)", "(\d+)[ ]+(total covid deaths)",
            "(\d+)[ ]+(total positive cases)", "(\d+)[ ]+(admitted in icu)", "(\d+)[ ]+(positivity rate)",
            "(\d+)[ ]+(case fatality rate)"
        ]
        PAGE_NUMBERS = self.pagemap[self._SUMMARY_KEY]

        page0 = extract_text(self.report_fpath, page_numbers=PAGE_NUMBERS)
        page0 = list(filter(lambda x: len(x.strip()) > 0, page0.split('\n')))   # extract non-empty line text as list
        
        dicttext = {}
        lastidx = -1

        for i, pageline in enumerate(page0):
            for regex in KEY_IDS:
                match = re.match(regex, pageline, re.IGNORECASE)

                if match:
                    idx = int(match.group(1))
                    text = match.group(2)                    
                    dicttext[idx] = text
                    lastidx = max(lastidx, i)

        numbers = page0[lastidx+1 : lastidx+1+len(dicttext)]

        result = {}
        for i, key in enumerate(sorted(dicttext.keys())):
            result[dicttext[key]] = self._str2num_(numbers[i])

        return result

    def _classify_vax_and_test_tables_(self, tablelist):
        vax_tablekeys = ['sessions planned', 'sessions held', 'total achievement']
        test_tablekeys = ['detection test', 'RT PCR', 'total test']

        col0_table = [row[0] for row in tablelist if type(row) == list]
        row0_table = tablelist[0]

        for col in col0_table:
            for key in vax_tablekeys:
                if key in col.strip().lower():
                    return 'vaccination'

        for row in row0_table:
            for key in test_tablekeys:
                if key in row.strip().lower():
                    return 'testing'
        
        return None

    def _extract_vax_and_test_tables_(self):

        PAGE_NUM = self.pagemap[self._VAX_AND_TEST_KEY]
        imgs = self._extract_imgs_(PAGE_NUM)
        img2table = TexTract()
        tables = {}

        for img in imgs:
            img_btyes = img.stream.get_rawdata()
            img_datalist = img2table.get_table_from_img(img_btyes)

            if img_datalist is None:
                continue 
            
            img_datalist = img_datalist[0]
            clf = self._classify_vax_and_test_tables_(img_datalist)
            tables[clf] = img_datalist

        return tables

    def _extract_district_vax_table_(self):
        
        if self._VAX_INFO_KEY not in self.pagemap:
            return None

        PAGE_NUM = self.pagemap[self._VAX_INFO_KEY]
        imgs = self._extract_imgs_(PAGE_NUM)
        img2table = TexTract()
        tables = []

        for img in imgs:
            img_btyes = img.stream.get_rawdata()
            img_datalist = img2table.get_table_from_img(img_btyes)

            if img_datalist is None:
                continue 
            
            img_datalist = img_datalist[0]
            tables.append(img_datalist)

        return tables

    def _extract_district_covid_table_(self):

        if self._DIST_COVID19_KEY not in self.pagemap:
            return None
        
        # Add 1 to page numbers due to different indexing by pdfminer (0-indexed) and camelot (1-indexed)
        pages_str = ','.join(map(lambda x: str(x+1), self.pagemap[self._DIST_COVID19_KEY]))
        tables = camelot.read_pdf(self.report_fpath, pages=pages_str, strip_text="\n")
        df = tables[0].df

        # TODO: Clean the district wise covid-19 table

        return df

    def _extract_todays_discharges_(self):
        pass

    def _extract_todays_deaths_(self):
        pass

    def _extract_icu_details_(self):

        if self._ICU_KEY not in self.pagemap:
            return None

        # Add 1 to page numbers due to different indexing by pdfminer (0-indexed) and camelot (1-indexed)
        pages_str = ','.join(map(lambda x: str(x+1), self.pagemap[self._ICU_KEY]))
        tables = camelot.read_pdf(self.report_fpath, pages=pages_str, strip_text="\n")
        df = tables[0].df

        # TODO: Clean the district wise covid-19 table

        return df

    def extract(self):

        case_summary = None # self._extract_summary_information_()
        vax_and_testing_tables = self._extract_vax_and_test_tables_()
        district_vax_table = self._extract_district_vax_table_()
        district_covid_table = self._extract_district_covid_table_()
        # self._extract_todays_discharges_()
        # self._extract_todays_deaths_()
        icu_table = self._extract_icu_details_()

        info = {
            'case-summary': case_summary,
            'vax-and-testing': vax_and_testing_tables,
            'district-vaccination': district_vax_table,
            'district-covid': district_covid_table,
            'today-discharges': None,
            'today-deaths': None,
            'icu-details': icu_table
        }

        return info



if __name__ == '__main__':
    fpath = '../../temp/notebooks/kt-sep3-20.pdf'
    obj = Karnataka(fpath)
    print(obj.pagemap)
    for x, y in obj.extract().items():
        print(x)
        if isinstance(y, pd.DataFrame):
            print(y.head())
        else:
            print(y)
        print('='*50)