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


    def __extract_district_tables(self, datatable, keyidxmap=None, major_key=0, find_total=False):

        if datatable is not None:
            result = []

            for district in self.list_of_districts:
                keymap = {district: [district.lower()]}

                new_result = {
                    'date'     : self.date,
                    'district' : district,
                }

                for key in keyidxmap:

                    minor_key = keyidxmap[key]
                    df_dict = common_utils.convert_df_to_dict(datatable, key_idx=major_key, val_idx=minor_key)

                    new_result[key] = common_utils.extract_info_from_table_by_keywords(df_dict, keymap).get(district, None)

                    try: new_result[key] = locale.atoi(new_result[key])
                    except: pass

                result.append(new_result)

            if find_total:

                total_key='total'
                keymap = {total_key: [total_key]}

                datatable = datatable.iloc[-1:]
                new_result = {
                    'date'     : self.date,
                    'district' : total_key,
                }

                for key in keyidxmap:

                    minor_key = keyidxmap[key]
                    df_dict = common_utils.convert_df_to_dict(datatable, key_idx=major_key, val_idx=minor_key)

                    new_result[key] = common_utils.extract_info_from_table_by_keywords(df_dict, keymap).get(total_key, None)

                    try: new_result[key] = locale.atoi(new_result[key])
                    except: pass

                result.append(new_result)

            return result


    def __extract_generic_datatable(self, datatable, keymap, transpose=False):

        if datatable is not None:

            if transpose:
                datatable = datatable.transpose()

            df_dict = common_utils.convert_df_to_dict(datatable, key_idx=0, val_idx=1)
            result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

            for key in result.keys():
                result[key] = locale.atoi(result[key])

            result['date'] = self.date
            return result


    def __extract_generic_datatables(self, datatables, key, keymap, transpose=False):

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

        keywords = {'positive cases declared today', 'declared negative today'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        keyidxmap = {
            'declared_positive': 1,
            'declared_negative': 2,
            'positive_cases_admitted': 3,
            'other_districts': 4
        }

        return self.__extract_district_tables(datatable, keyidxmap, major_key=0, find_total=True)


    def extract_district_death_info(self, tables):

        keywords = {'no of deaths reported daily', 'district'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        keyidxmap = {
            'deaths_reported': 1,
            'death_through_appeal': 2,
            'pending_deaths': 3,
            'death_cases_approved': 4
        }

        return self.__extract_district_tables(datatable, keyidxmap, major_key=0, find_total=True)


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

        keywords = {'gender', 'death date'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is not None:
            result = []

            for index, row in datatable.iterrows():
                result.append({
                        'name': row[2],
                        'district': row[1],
                        'place': row[3],
                        'age': row[4],
                        'gender': row[5],
                        'death_date': row[6]
                    })

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

        keywords = {'quarantine', 'observation', 'isolation', 'district'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        keyidxmap = {
            'cumulative_under_observation': 1,
            'cumulative_under_home_isolation': 2,
            'cumulative_hospitalized': 3,
            'new_hospitalized': 4
        }

        return self.__extract_district_tables(datatable, keyidxmap, major_key=0, find_total=True)


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

        if datatable is not None:
            datatable = datatable.iloc[2:]

            keyidxmap = {
                'LSG': 2,
                'Wards': 3
            }

            return self.__extract_district_tables(datatable, keyidxmap, major_key=1, find_total=True)


    def extract(self):

        all_tables_camelot = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        result = {
            'contact-travel-cumulative': self.extract_contact_travel_cumulative(all_tables_camelot),
            'contact-travel-new': self.extract_contact_travel_new(all_tables_camelot),
            'critical-patients': self.extract_critical_patients(all_tables_camelot),
            'cumulative-summary-t-minus-one': self.extract_cumulative_summary_t_minus_one(all_tables_camelot),
            'cumulative-summary': self.extract_cumulative_summary(all_tables_camelot),
            'daily-summary': self.extract_daily_summary(all_tables_camelot),
            'district-abstract': self.extract_district_abstract(all_tables_camelot),
            'district-case-info': self.extract_district_case_info(all_tables_camelot),
            'district-death-info': self.extract_district_death_info(all_tables_camelot),
            'individual-death-info': self.extract_individual_death_info(all_tables_camelot),
            'psychosocial-support': self.extract_psychosocial_support(all_tables_camelot),
            'surveillance-info': self.extract_surveillance_info(all_tables_camelot),
            'testing-cumulative': self.extract_cumulative_tests(all_tables_camelot),
            'testing-new': self.extract_new_tests(all_tables_camelot),
            'travel-surveillance': self.extract_travel_surveillance(all_tables_camelot),
        }

        return result


if __name__ == '__main__':

    date = '2021-10-29'
    path = "../localstore_KL/bulletins/KL/KL-Bulletin-2021-10-01.pdf"

    obj = KeralaExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())

