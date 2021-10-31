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


class KeralaExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        self.list_of_districts = [
            "Thiruvananthapuram",
            "Kollam",
            "Pathanamthitta",
            "Alappuzha",
            "Kottayam",
            "Idukki",
            "Ernakulam",
            "Thrissur",
            "Palakkad",
            "Malappuram",
            "Kozhikode",
            "Wayanad",
            "Kannur",
            "Kasaragod"
        ]


    def extract_cumulative_summary_t_minus_one(self, tables):
        result = {}

        # for table in tables:
        #     print(666, table, dir(table))

        # datatable = None
        # keywords = {'Positive cases'}
        # datatable = common_utils.find_table_by_keywords(tables, keywords)

        # if datatable is None:
        #     return None

        return result


    def extract_daily_summary(self, tables):
        result = {}
        return result


    def extract_cumulative_summary(self, tables):
        result = {}
        return result


    def extract_district_case_info(self, tables):
        result = {}
        return result


    def extract_district_death_info(self, tables):
        result = {}
        return result


    def extract_contact_travel_cumulative(self, tables):
        result = {}
        return result


    def extract_contact_travel_new(self, tables):
        result = {}
        return result


    def extract_individual_death_info(self, tables):
        result = {}
        return result


    def extract_critical_patients(self, tables):
        result = {}
        return result


    def extract_cumulative_tests(self, tables):
        result = {}
        return result


    def extract_new_tests(self, tables):
        result = {}
        return result


    def extract_surveillance_info(self, tables):
        result = {}
        return result


    def extract_travel_surveillance(self, tables):
        result = {}
        return result


    def extract_psychosocial_support(self, tables):

        keywords = {'psychosocial', 'children', 'alone'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        else:

            df_dict = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=1)
            keymap = {
                'psychosocial_workers': ['psychosocial', 'workers', 'no.'],
                'calls_to_persons_in_surveillance': ['quarantine', 'isolation'],
                'followup_calls': ['follow-up'],
                'post_covid_calls': ['post covid'],
                'calls_special': ['migrant', 'alone'],
                'calls_to_school_children': ['school'],
                'calls_to_health_care_workers': ['health care workers'],
                'calls_received_helpline': ['helpline'],
                'calls_total': ['all categories']
            }

            result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

            for key in result.keys():
                result[key] = locale.atoi(result[key])

            result['date'] = self.date
            return result


    def extract_district_abstract(self, tables):

        keywords = {'wipr (> 10)'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        else:

            result = []
            datatable = datatable.iloc[2:]

            df_dict_lsg = common_utils.convert_df_to_dict(datatable, key_idx=1, val_idx=2)
            df_dict_ward = common_utils.convert_df_to_dict(datatable, key_idx=1, val_idx=3)

            for district in self.list_of_districts:
                keymap = {district: [district.lower()]}

                new_result = {
                    'date'     : self.date,
                    'district' : district,
                    'LSG'      : locale.atoi(common_utils.extract_info_from_table_by_keywords(df_dict_lsg, keymap).get(district, None)),
                    'Wards'    : locale.atoi(common_utils.extract_info_from_table_by_keywords(df_dict_ward, keymap).get(district, None)),
                }

                result.append(new_result)

            # adding total column
            datatable = datatable.iloc[-1:]

            df_dict_lsg = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=2)
            df_dict_ward = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=3)

            keymap = {'total': ['grand total']}
            new_result = {

                'date'     : self.date,
                'district' : 'Grand Total',
                'LSG'      : locale.atoi(common_utils.extract_info_from_table_by_keywords(df_dict_lsg, keymap).get('total', None)),
                'Wards'    : locale.atoi(common_utils.extract_info_from_table_by_keywords(df_dict_ward, keymap).get('total', None)),
            }

            result.append(new_result)
            return result


    def extract(self):

        all_tables_camelot = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        result = {
            'cumulative-summary-t-minus-one': self.extract_cumulative_summary_t_minus_one(all_tables_camelot),
            'daily-summary': self.extract_daily_summary(all_tables_camelot),
            'cumulative-summary': self.extract_cumulative_summary(all_tables_camelot),
            'district-case-info': self.extract_district_case_info(all_tables_camelot),
            'district-death-info': self.extract_district_death_info(all_tables_camelot),
            'contact-travel-cumulative': self.extract_contact_travel_cumulative(all_tables_camelot),
            'contact-travel-new': self.extract_contact_travel_new(all_tables_camelot),
            'individual-death-info': self.extract_individual_death_info(all_tables_camelot),
            'critical-patients': self.extract_critical_patients(all_tables_camelot),
            'testing-cumulative': self.extract_cumulative_tests(all_tables_camelot),
            'testing-new': self.extract_new_tests(all_tables_camelot),
            'surveillance-info': self.extract_surveillance_info(all_tables_camelot),
            'travel-surveillance': self.extract_travel_surveillance(all_tables_camelot),
            'psychosocial-support': self.extract_psychosocial_support(all_tables_camelot),
            'district-abstract': self.extract_district_abstract(all_tables_camelot),
        }

        return result


if __name__ == '__main__':

    date = '2021-10-29'
    path = "/Users/tchakra2/Desktop/Bulletin-HFWD-English-October-29.pdf"

    obj = KeralaExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())

