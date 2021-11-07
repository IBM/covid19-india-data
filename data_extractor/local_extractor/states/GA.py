import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class GoaExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath


    def extract_active_cases(self, tables):
        datatable = common_utils.find_table_by_keywords(tables, "travellers by (road,flight,train)")

        if datatable is not None:

            datatable = datatable.iloc[1:]
            result = list()

            df_dict_north = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=1)
            df_dict_south = common_utils.convert_df_to_dict(datatable, key_idx=2, val_idx=3)

            for item in df_dict_north:

                district = "NORTH"

                if "travellers" in item.lower():
                    district = None

                result.append({
                    "date"     : self.date,
                    "location" : item, 
                    "district" : district, 
                    "cases"    : locale.atoi(df_dict_north[item]), 
                })

            for item in df_dict_south:
                result.append({
                    "date"     : self.date,
                    "location" : item, 
                    "district" : "SOUTH", 
                    "cases"    : locale.atoi(df_dict_south[item]), 
                })

            return result


    def extract_bed_capacity(self, tables):
        # NEEDS IMAGE EXTRACTION #
        pass


    def extract_overview(self, tables):
        # NEEDS IMAGE EXTRACTION #

        active_cases_info = self.extract_active_cases(tables)
        active_cases = 0 

        for item in active_cases_info:
            active_cases += item["cases"]

        return {
            "active_cases" : active_cases,
        }


    def extract(self):

        all_tables_camelot = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        result = {
            'overview': self.extract_overview(all_tables_camelot),
            'active-cases': self.extract_active_cases(all_tables_camelot),
            'bed-capacity': self.extract_bed_capacity(all_tables_camelot),
        }

        return result


if __name__ == '__main__':

    date = '2020-10-10'
    path = "/Users/tchakra2/Desktop/Media-Bulletin-10-October-2020.pdf"

    # date = '2021-11-07'
    # path = "/Users/tchakra2/Desktop/Media-Bulletin-3RD-AUG-2021.pdf"

    obj = GoaExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())

