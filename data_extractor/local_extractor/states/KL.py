import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import dateparser

try:
    from local_extractor.utils import common_utils
    from local_extractor.utils.table_concatenation import concatenate_tables
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils
    from utils.table_concatenation import concatenate_tables


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

        keywords = {'positive', 'case', 'recovered', 'quarantine', 'isolation', 'home', 'hospital', 'death'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'positive_cases': ['positive', 'cases'],
            'recovered': ['recovered'],
            'new_persons_in_surveillance': ['new', 'person', 'quarantine', 'isolation'],
            'new_persons_in_home_ins_isolation': ['new', 'person', 'home', 'quarantine'],
            'new_persons_in_hospital_isolation': ['new', 'person', 'hospital', 'isolation'],
            # 'daily_deaths': ['deaths'],
            'deaths_declared_as_per_appeal': ['deaths declared as per appeal'],
            'pending_deaths': ['pending deaths']
        }

        result = self.__extract_generic_datatables(datatables, 0, keymap, transpose=True)
        
        # TODO: Cheap fix. Need to modify
        result['daily_deaths'] = None
        tbl = datatables[0]
        daily_deaths_header = tbl[5][0]
        daily_deaths_val = tbl[5][1]

        if 'deaths' in daily_deaths_header.lower():
            result['daily_deaths'] = locale.atoi(daily_deaths_val)

        return result


    def extract_daily_summary(self, tables):

        keywords = {'positive', 'case', 'recovered', 'quarantine', 'isolation', 'home', 'hospital', 'death'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'positive_cases': ['positive', 'cases'],
            'recovered': ['recovered'],
            'new_persons_in_surveillance': ['new', 'person', 'quarantine', 'isolation'],
            'new_persons_in_home_ins_isolation': ['new', 'person', 'home', 'quarantine'],
            'new_persons_in_hospital_isolation': ['new', 'person', 'hospital', 'isolation'],
            # 'daily_deaths': ['deaths'],
            'deaths_declared_as_per_appeal': ['deaths declared as per appeal'],
            'pending_deaths': ['pending deaths']
        }

        result = self.__extract_generic_datatables(datatables, 1, keymap, transpose=True)

        # TODO: Cheap fix. Need to modify
        result['daily_deaths'] = None
        tbl = datatables[1]
        daily_deaths_header = tbl[5][0]
        daily_deaths_val = tbl[5][1]

        if 'deaths' in daily_deaths_header.lower():
            result['daily_deaths'] = locale.atoi(daily_deaths_val)

        return result


    def extract_cumulative_summary(self, tables):

        keywords = {'positive', 'case', 'recovered', 'quarantine', 'isolation', 'home', 'hospital', 'death'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'total_positive_cases': ['positive', 'cases'],
            'active_cases': ['active', 'cases'],
            'total_recovered': ['recovered'],
            'total_persons_in_surveillance': ['persons', 'quarantine', 'isolation'],
            'total_persons_in_home_ins_isolation': ['persons', 'home', 'institution', 'quarantine'],
            'total_persons_in_hospital_isolation': ['persons', 'hospital'],
            # 'total_deaths': ['deaths'],
            'total_deaths_declared_as_per_appeal': ['deaths declared as per appeal'],
            'total_pending_deaths': ['pending deaths']
        }

        result = self.__extract_generic_datatables(datatables, 2, keymap, transpose=True)

        # TODO: Cheap fix. Need to modify
        result['total_deaths'] = None
        tbl = datatables[2]
        daily_deaths_header = tbl[6][0]
        daily_deaths_val = tbl[6][1]

        if 'deaths' in daily_deaths_header.lower():
            result['total_deaths'] = locale.atoi(daily_deaths_val)

        return result


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
        
        keywords = {'international', 'interstate', 'travel', 'contact', 'history'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'total_cases': ['total cases'],
            'history_of_travel': ['history', 'international/interstate', 'travel'],
            'history_of_contact': ['history', 'contact']
        }

        return self.__extract_generic_datatables(datatables, 0, keymap)


    def extract_contact_travel_new(self, tables):

        keywords = {'international', 'interstate', 'travel', 'contact', 'history'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'total_cases': ['total cases'],
            'history_of_travel': ['history', 'international/interstate', 'travel'],
            'history_of_contact': ['history', 'contact'],
            'no_history': ['no', 'history', 'travel']
        }

        return self.__extract_generic_datatables(datatables, 1, keymap)


    def extract_individual_death_info(self, tables):

        def convert_header_text_to_colname(datadict, keymap):
            datadict_new = {}
            processed_colnames = []

            for text, val in datadict.items():
                for colname, keys in keymap:

                    if False in [key in text.lower() for key in keys] or colname in processed_colnames:
                        continue
                        
                    datadict_new[colname] = val
                    processed_colnames.append(colname)
                
            return datadict_new


        keywords = {'district', 'age', 'date', 'death'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        # convert dataframe into a dictionary
        datalist = [list(row) for _, row in datatable.iterrows()]
        datadict = {}
        cols = datalist[0]

        for rownum in range(1, len(datalist)):
            for colnum, col in enumerate(cols):
                if col not in datadict:
                    datadict[col] = []

                datadict[col].append(datalist[rownum][colnum])


        header_keymap = [
            ('district', ['district']),
            ('name', ['name']),
            ('place', ['place']),
            ('age', ['age']),
            ('gender', ['gender']),
            ('gender', ['sex']),
            ('death_date', ['date', 'death'])
        ]

        datadict = convert_header_text_to_colname(datadict, header_keymap)

        result = []
        cols = list(datadict.keys())
        n = len(datadict[cols[0]])

        for i in range(n):

            try:
                row = {col: datadict[col][i] for col in cols}

                row['date'] = self.date

                if 'death_date' in row:
                    date = dateparser.parse(row['death_date'].strip(), ['%d-%m-%Y'])
                    row['death_date'] = f'{date.year}-{date.month:02d}-{date.day:02d}'

                if 'age' in row:
                    row['age'] = locale.atoi(row['age'].strip())
            except:
                pass
            else:
                result.append(row)

        return result


    def extract_critical_patients(self, tables):

        keywords = {'icus', 'ventilator', 'support', 'patient'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        keymap = {
            'patients_in_icu': ['icus'],
            'patients_on_ventillation': ['ventilator', 'support']
        }

        return self.__extract_generic_datatable(datatable, keymap)


    def extract_cumulative_tests(self, tables):

        keywords = {'samples', 'sent', 'naat', 'antigen'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'samples_sent': ['samples sent'],
            'routine_sentinel_samples_pcr': ['sentinel'],
            'airport_surveillance': ['surveillance'],
            'CB_NAAT': ['cb', 'naat'],
            'True_NAT': ['true', 'nat'],
            'POCT_PCR': ['poct', 'pcr'],
            'RT_LAMP': ['lamp'],
            'Antigen_Assay': ['assay']
        }

        return self.__extract_generic_datatables(datatables, 0, keymap, transpose=True)


    def extract_new_tests(self, tables):

        keywords = {'samples', 'sent', 'naat', 'antigen'}
        datatables = common_utils.find_all_tables_by_keywords(tables, keywords)

        keymap = {
            'samples_sent': ['samples sent'],
            'routine_sentinel_samples_pcr': ['sentinel'],
            'airport_surveillance': ['surveillance'],
            'CB_NAAT': ['cb', 'naat'],
            'True_NAT': ['true', 'nat'],
            'POCT_PCR': ['poct', 'pcr'],
            'RT_LAMP': ['lamp'],
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

        keywords = {'travel', 'mode'}
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
            'psychosocial_workers': ['psychosocial', 'workers', 'no'],
            'calls_to_persons_in_surveillance': ['quarantine', 'isolation'],
            'followup_calls': ['follow', 'up', 'calls'],
            'post_covid_calls': ['post', 'covid', 'calls'],
            'calls_special': ['migrant', 'alone', 'mental', 'illness', 'different', 'able'],
            'calls_to_school_children': ['school', 'children'],
            'calls_to_health_care_workers': ['health', 'care', 'workers'],
            'calls_received_helpline': ['calls', 'received', 'helpline'],
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

        # do not parse bulletins prior to June 1st, 2020
        if self.date < "2020-06-01":
            return dict()

        all_tables_camelot = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, split_text=False)
        all_tables_camelot_joined = concatenate_tables.concatenate_tables(all_tables_camelot, 'same-table-width')

        result = {
            'contact-travel-cumulative': self.extract_contact_travel_cumulative(all_tables_camelot),
            'contact-travel-new': self.extract_contact_travel_new(all_tables_camelot),
            'critical-patients': self.extract_critical_patients(all_tables_camelot),
            'cumulative-summary-t-minus-one': self.extract_cumulative_summary_t_minus_one(all_tables_camelot),
            'cumulative-summary': self.extract_cumulative_summary(all_tables_camelot),
            'daily-summary': self.extract_daily_summary(all_tables_camelot),
            'district-abstract': self.extract_district_abstract(all_tables_camelot_joined),
            'district-case-info': self.extract_district_case_info(all_tables_camelot),
            'district-death-info': self.extract_district_death_info(all_tables_camelot),        # not available in all bulletins (29-Oct-2021)
            'individual-death-info': self.extract_individual_death_info(all_tables_camelot_joined),
            'psychosocial-support': self.extract_psychosocial_support(all_tables_camelot),
            'surveillance-info': self.extract_surveillance_info(all_tables_camelot),
            'testing-cumulative': self.extract_cumulative_tests(all_tables_camelot),
            'testing-new': self.extract_new_tests(all_tables_camelot),
            'travel-surveillance': self.extract_travel_surveillance(all_tables_camelot),
        }

        return result


if __name__ == '__main__':

    date = '2021-10-29'
    path = "/home/mayankag/covid19-india-data/localstore/bulletins/KL/KL-Bulletin-2021-11-21.pdf"

    obj = KeralaExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())

