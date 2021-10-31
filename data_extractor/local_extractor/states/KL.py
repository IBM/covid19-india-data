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

    def __extract_district_tables(self, datatable, keymap = None, keywords = None):
        pass


    def __extract_generic_datatable(self, datatable, keymap, transpose = False):

        if datatable is not None:

            if transpose:
                datatable = datatable.transpose()

            df_dict = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=1)
            result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

            for key in result.keys():
                result[key] = locale.atoi(result[key])

            result['date'] = self.date
            return result


    def __extract_generic_datatables(self, datatables, key, keymap, transpose = False):

        if datatables: 
            return self.__extract_generic_datatable(datatables[key], keymap, transpose)


    def extract_cumulative_summary_t_minus_one(self, tables):

        keywords = {'no of deaths declared as per appeal'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'positive_cases': ['positive cases'],
            'recovered': ['recovered'],
            'new_persons_in_surveillance': ['persons in quarantine'],
            'new_persons_in_home_ins_isolation': ['persons in home'],
            'new_persons_in_hospital_isolation': ['persons in hospital'],
            'daily_deaths': ['no of deaths reported daily'],
            'deaths_declared_as_per_appeal': ['no of deaths declared as per appeal'],
            'pending_deaths': ['no of pending deaths']
        }

        return self.__extract_generic_datatables(datatables, 0, keymap, transpose=True)


    def extract_daily_summary(self, tables):

        keywords = {'no of deaths declared as per appeal'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'positive_cases': ['positive cases'],
            'recovered': ['recovered'],
            'new_persons_in_surveillance': ['persons in quarantine'],
            'new_persons_in_home_ins_isolation': ['persons in home'],
            'new_persons_in_hospital_isolation': ['persons in hospital'],
            'daily_deaths': ['no of deaths reported daily'],
            'deaths_declared_as_per_appeal': ['no of deaths declared as per appeal'],
            'pending_deaths': ['no of pending deaths']
        }

        return self.__extract_generic_datatables(datatables, 1, keymap, transpose=True)


    def extract_cumulative_summary(self, tables):

        keywords = {'no of deaths declared as per appeal'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'total_positive_cases': ['positive cases'],
            'active_cases': ['active cases'],
            'total_recovered': ['recovered'],
            'total_persons_in_surveillance': ['persons in quarantine'],
            'total_persons_in_home_ins_isolation': ['persons in home'],
            'total_persons_in_hospital_isolation': ['persons in hospital'],
            'total_deaths': ['total no of deaths', '(d)'],
            'total_deaths_declared_as_per_appeal': ['no of deaths declared as per appeal'],
            'total_pending_deaths': ['no of pending deaths']
        }

        return self.__extract_generic_datatables(datatables, 2, keymap, transpose=True)


    def extract_district_case_info(self, tables):
        result = {}
        return result


    def extract_district_death_info(self, tables):
        result = {}
        return result


    def extract_contact_travel_cumulative(self, tables):
        
        keywords = {'history of international/interstate travel'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'total_cases': ['total cases'],
            'history_of_travel': ['history of international/interstate travel'],
            'history_of_contact': ['history of contact']
        }

        return self.__extract_generic_datatables(datatables, 0, keymap)


    def extract_contact_travel_new(self, tables):

        keywords = {'history of international/interstate travel'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'total_cases': ['total cases'],
            'history_of_travel': ['history of international/interstate travel'],
            'history_of_contact': ['history of contact'],
            'no_history': ['no history']
        }

        return self.__extract_generic_datatables(datatables, 1, keymap)


    def extract_individual_death_info(self, tables):
        result = {}
        return result


    def extract_critical_patients(self, tables):

        keywords = {'icus', 'ventilator support'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        keymap = {
            'patients_in_icu': ['icus'],
            'patients_on_ventillation': ['ventilator support']
        }

        return self.__extract_generic_datatable(datatable, keymap)


    def extract_cumulative_tests(self, tables):

        keywords = {'samples sent', 'cb naat'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'samples_sent': ['samples sent'],
            'routine_sentinel_samples_pcr': ['sentinel'],
            'airport_surveillance': ['surveillance'],
            'CB_NAAT': ['cb naat'],
            'True_NAT': ['true nat'],
            'POCT_PCR': ['poct pcr'],
            'RT_LAMP': ['rl lamp'],
            'Antigen_Assay': ['assay']
        }

        return self.__extract_generic_datatables(datatables, 0, keymap, transpose=True)


    def extract_new_tests(self, tables):

        keywords = {'samples sent', 'cb naat'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'samples_sent': ['samples sent'],
            'routine_sentinel_samples_pcr': ['sentinel'],
            'airport_surveillance': ['surveillance'],
            'CB_NAAT': ['cb naat'],
            'True_NAT': ['true nat'],
            'POCT_PCR': ['poct pcr'],
            'RT_LAMP': ['rl lamp'],
            'Antigen_Assay': ['assay']
        }

        return self.__extract_generic_datatables(datatables, 1, keymap, transpose=True)


    def extract_surveillance_info(self, tables):
        result = {}
        return result


    def extract_travel_surveillance(self, tables):

        keywords = {'mode of travel'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        keymap = {
            'international_cumulative': ['international'],
            'domestic_cumulative': ['domestic'],
            'total': ['total']
        }

        return self.__extract_generic_datatable(datatable, keymap)


    def extract_psychosocial_support(self, tables):

        keywords = {'psychosocial', 'children', 'alone'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

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

        return self.__extract_generic_datatable(datatable, keymap)


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
    path = "/Users/tchakra2/Desktop/Bulletin-HFWD-English-October-30.pdf"

    obj = KeralaExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())

