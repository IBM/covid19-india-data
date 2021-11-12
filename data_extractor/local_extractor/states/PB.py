import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pandas as pd
import camelot

import pdfminer
from pdfminer.high_level import extract_pages
import pdb

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class PunjabExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

        # for matching 3(Amritsar-1, Ludhiana-2)
        self.district_regex = re.compile(r'([\d]+)\(([\d,\D,\s]+)\)')
        self.empty_keywords = ["nil", "----"]
        self.extra_char = ['*', '%']

    def _process_district_info_(self, data, col, new_cols, del_old=False):
        if col in data:
            m = self.district_regex.match(data[col])
            if m:
                parsed = m.groups()
                data[new_cols[0]] = parsed[0]
                data[new_cols[1]] = parsed[1]

            if del_old:
                del data[col]

        return data

    def _clean_empty_values_(self, data, cols = None, _format = "INT"):
        # format is integer for INT or STR for string
        # in case of INT 0 is stored and in case of STR empty string is saved
        cols = data.keys() if not cols else cols

        for keyword in self.empty_keywords:
            for col in cols:
                if col in data and keyword in data[col].strip().lower():
                    if _format == "INT":
                        data[col] = str(0)
                    elif _format == "STR":
                        data[col] = ""

        return data

    def _clear_extra_char_(self, data, cols = None):
        cols = data.keys() if not cols else cols

        for col in cols:
            for ch in self.extra_char:
                if col in data:
                    data[col] = data[col].replace(ch, "")

        return data

    def _find_index_by_column_(self, tables, keywords):
        # matches keywords from the table columns
        # returns the index in the list of tables
        # returns -1 if table not found
        for index, table in enumerate(tables):
            df_tab = table.df
            copy_keywords = []
            copy_keywords = keywords.copy()
            for i in range(len(copy_keywords) -1, -1, -1):
                for col in df_tab:
                    keyword = copy_keywords[i]
                    if keyword in df_tab[col][0].strip().lower():
                        copy_keywords.remove(copy_keywords[i])
                        break

            if len(copy_keywords) == 0:
                return index

        return -1


    def extract_cases_info(self, tables):
        info_table = None
        keywords = {'samples', 'vaccination', 'conducted', 'discharged'}

        info_table = common_utils.find_table_by_keywords(tables, keywords)

        if info_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(info_table, key_idx=1, val_idx=2)
        keymap = {
            'samples_total': ['total', 'samples', 'taken'],
            'samples_new': ['sample', 'collected', 'day'],
            'tests_new': ['test', 'conducted', 'day'],
            'cases_total': ['patiens', 'tested', 'positive'],
            'discharged_total': ['patients', 'discharged'],
            'active_cases': ['number', 'active', 'cases'],
            'deaths_total': ['total', 'deaths', 'reported'],
            'oxygen_support_active_patients': ['patients', 'oxygen', 'support'],
            'critical_care_active_patients': ['critical', 'care', 'level-3', 'facilities'],
            'ventilator_support_active_patients': ['critical', 'ventilator', 'support'],
            'healthcare_first_vaccination_today': ['healthcare', 'vaccinated', '1st', 'dose', 'day'],
            'healthcare_first_vaccination_total': ['total', 'healthcare', 'vaccinated', '1st', 'dose'],
            'frontline_first_vaccination_today': ['frontline', 'vaccinated', '1st', 'dose', 'day'],
            'frontline_first_vaccination_total': ['total', 'frontline', 'vaccinated', '1st', 'dose'],
            'healthcare_second_vaccination_today': ['healthcare', 'vaccinated', '2nd', 'dose', 'day'],
            'healthcare_second_vaccination_total': ['total', 'healthcare', 'vaccinated', '2nd', 'dose'],
            'frontline_second_vaccination_today': ['frontline', 'vaccinated', '2nd', 'dose', 'day'],
            'frontline_second_vaccination_total': ['total', 'frontline', 'vaccinated', '2nd', 'dose'],
            'above_45_first_vaccination_today': ['above', '45', 'vaccinated', '1st', 'dose', 'day'],
            'above_45_first_vaccination_total': ['total', 'above', '45', 'vaccinated', '1st', 'dose'],
            'above_45_second_vaccination_today': ['above', '45', 'vaccinated', '2nd', 'dose', 'day'],
            'above_45_second_vaccination_total': ['total', 'above', '45', 'vaccinated', '2nd', 'dose'],
            'eighteen_44_first_vaccination_today': ['18-44', 'vaccinated', '1st', 'dose', 'day'],
            'eighteen_44_first_vaccination_total': ['total', '18-44', 'vaccinated', '1st', 'dose'],
            'eighteen_44_second_vaccination_today': ['18-44', 'vaccinated', '2nd', 'dose', 'day'],
            'eighteen_44_second_vaccination_total': ['total', '18-44', 'vaccinated', '2nd', 'dose'],
            'first_vaccination_today': ['total', '1st', 'vaccination', 'dose', 'day'],
            'second_vaccination_today': ['total', '2nd', 'vaccination', 'dose', 'day'],
            'total_vaccination_today': ['total', '1st', 'and', '2nd', 'vaccination', 'dose', 'day']
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        # clean result
        cols = result.keys()
        result = self._clean_empty_values_(result)
        result = self._clear_extra_char_(result, cols)

        for col in result.keys():
            result[col] = locale.atoi(result[col])

        result["date"] = self.date

        return result

    def extract_patient_info(self, tables):
        info_table = None
        keywords = {"icu", "ventilator", "discharged", "deaths"}

        info_table = common_utils.find_table_by_keywords(tables, keywords)

        if info_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(info_table, key_idx=1, val_idx=2)

        keymap = {
            'icu_patients_today': ["admitted", "icu"],
            'ventilator_patients_today': ["put", "ventilator", "support"],
            'discharged_patients_today': ["patients", "discharged"],
            'deaths_today': ["deaths", "reported"]
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        # clean up the data
        result = self._process_district_info_(result, 'icu_patients_today', ["icu_patients_today", "icu_patients_today_districts"])
        result = self._process_district_info_(result, 'ventilator_patients_today', ["ventilator_patients_today", "ventilator_patients_today_districts"])
        result = self._process_district_info_(result, 'discharged_patients_today', ["discharged_patients_today", "discharged_patients_today_districts"])
        result = self._process_district_info_(result, 'deaths_today', ["deaths_today", "deaths_today_districts"])

        cols = keymap.keys()
        result = self._clean_empty_values_(result, cols, "INT")
        result = self._clear_extra_char_(result, cols)

        str_cols = ["icu_patients_today_districts", "ventilator_patients_today_districts", "discharged_patients_today_districts", "deaths_today_districts"]
        result = self._clean_empty_values_(result, str_cols, "STR")

        for col in cols:
            result[col] = locale.atoi(result[col])

        result["date"] = self.date

        return result


    def extract_district_info(self, tables):
        if not tables:
            return None

        keywords_recent = ["positivity", "remarks", "details"]
        keywords_old = ["source", "infection", "remarks", "details"]
        is_source_present = True # true means the second column is a string
        # in recent bulletins it is a different column with float value

        df_init = None
        df_init = common_utils.find_table_by_keywords(tables, keywords_recent)
        district_data = dict()
        all_sub_tables_parsed = False

        if df_init is None:
            df_init = common_utils.find_table_by_keywords(tables, keywords_old)
            keywords = keywords_old
        else:
            is_source_present = False
            keywords = keywords_recent

        total_district = ""

        if df_init is not None:
            df_init = df_init.iloc[1:]
            tab_counter = 0
            index_df = self._find_index_by_column_(tables, keywords)
            if index_df == -1:
                print("something went wrong, init table not found")
            number_cols = df_init.shape[1]

            while not all_sub_tables_parsed:
                # sanity check whether the next table is the same shape
                # if it is not the same shape that would mean it is cumulative data
                if number_cols != df_init.shape[1]:
                    break

                for i, row in df_init.iterrows():
                    row = [x for x in list(row) if x]

                    if len(row) <= 1:
                        continue

                    if "day" in row[0].strip().lower():
                        # this will tell me that whether next table
                        # is table with district cases or not
                        all_sub_tables_parsed = True
                        total_district = row[0].strip().lower()

                    district = row[0].strip().lower()
                    cases_today = row[1].strip()
                    source_positive_percentage = row[2].strip()
                    if not all_sub_tables_parsed:
                        details = row[3].strip().lower()
                        remarks = row[4].strip().lower()
                    else:
                        details = ""
                        remarks = ""

                    tmp = {
                        "date": self.date,
                        "district": district,
                        "cases_today": cases_today,
                        "case_details": details,
                        "remarks": remarks
                    }

                    if is_source_present:
                        tmp["outside_source_details"] = source_positive_percentage.lower()
                    else:
                        tmp["percentage_tests_positive"] = source_positive_percentage

                    tmp = self._clean_empty_values_(tmp, ["case_details", "remarks", "outside_source_details"], "STR")
                    district_data[district] = tmp

                tab_counter += 1
                df_init = tables[index_df + tab_counter].df

        keywords_cumulative = ["confirmed", "active", "cured", "deaths"]
        df_cumulative = None
        df_cumulative = common_utils.find_table_by_keywords(tables, keywords_cumulative)

        stop_loop = False
        if df_cumulative is None:
            df_cumulative = df_cumulative.iloc[1:]

            for i, row in df_cumulative.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if len(row) <= 1:
                    continue

                if "total" in row[1].strip().lower():
                    stop_loop = True
                    cumulative_total = row[1].strip().lower()

                district = row[1].strip().lower()
                confirmed = row[2].strip()
                active = row[3].strip()
                cured = row[4].strip()
                deaths = row[5].cases()

                tmp = {
                    "date": self.date,
                    "district": district,
                    "cases_total": confirmed,
                    "active_cases": active,
                    "recovered_total": cured,
                    "deaths_total": deaths
                }

                if district in district_data:
                    district_data[district].update(tmp)
                elif stop_loop and not total_district:
                    district_data[total_district].update(tmp)
                else:
                    district_data[district] = tmp

        # clean the complete data
        int_cols = ["cases_today", "cases_total", "active_cases", "recovered_total", "deaths_total"]
        str_cols = ["outside_source_details", "case_details", "remarks"]
        float_cols = ["percentage_tests_positive"]
        char_cols = int_cols.copy()
        char_cols.extend(float_cols)
        result = list()
        for key, val in district_data.items():
            val = self._clear_extra_char_(val, char_cols)
            val = self._clean_empty_values_(val, int_cols, "INT")
            val = self._clean_empty_values_(val, str_cols, "STR")

            for col in int_cols:
                if col in val:
                    val[col] = locale.atoi(val[col])

            result.append(val)

            for col in float_cols:
                if col in val:
                    val[col] = locale.atof(val[col])

        return result

    def extract_micro_containment_zone_info(self, tables):
        keywords = ["micro", "containment", "population"]
        keywords_old = ["high", "priority", "population"]
        df_micro = None
        df_micro = common_utils.find_table_by_keywords(tables, keywords)

        if df_micro is None:
            df_micro = common_utils.find_table_by_keywords(tables, keywords_old)
            keywords = keywords_old

        if df_micro is None:
            return None

        index = self._find_index_by_column_(tables, keywords)
        if index == -1:
            print("something went wrong, micro containment table index not found")

        stop_loop = False
        counter = 1
        result = list()
        df_micro = df_micro.iloc[1:]
        current_district = ""
        number_cols = df_micro.shape[1]
        while not stop_loop:
            if number_cols != df_micro.shape[1]:
                break

            # this iterates over tables
            tmp, current_district, stop_loop = self._parse_containment_info_(df_micro, current_district)
            result.extend(tmp)
            df_micro = tables[index + counter].df

        return result

    def extract_large_containment_zone_info(self, tables):
        keywords = ["containment", "population", "total"]
        keywords_old = ["large", "outbreak", "total"]
        df_containe = None
        df_contain = common_utils.find_table_by_keywords(tables, keywords)

        if df_contain is None:
            df_contain = common_utils.find_table_by_keywords(tables, keywords_old)
            keywords = keywords_old

        if df_contain is None:
            return None

        index = self._find_index_by_column_(tables, keywords)
        if index == -1:
            print("something went wrong, containment table index not found")

        stop_loop = False
        counter = 1
        result = list()
        df_contain = df_contain.iloc[1:]
        current_district = ""
        number_cols = df_contain.shape[1]
        while not stop_loop:
            if number_cols != df_contain.shape[1]:
                break

            # this iterates over tables
            tmp, current_district, stop_loop = self._parse_containment_info_(df_contain, current_district)
            result.extend(tmp)
            df_contain = tables[index + counter].df

        return result


    def _parse_containment_info_(self, table, _district = ""):
        # type is the containment type can be micro or large
        stop_loop = False
        number_cols = table.shape[1]
        district = _district
        result = list()

        for i, row in table.iterrows():
            row = [x for x in list(row) if x]

            if len(row) <= 1:
                continue

            if "total" in row[1].strip().lower() or "total" in row[0].strip().lower():
                stop_loop = True
                break

            if len(row) == number_cols:
                district = row[1].strip().lower()

            zone = row[-2].strip().lower()
            population = row[-1].strip().lower()
            tmp = {
                "date": self.date,
                "district": district,
                "containment": zone,
                "population_contained": population
            }

            cols = ["population_contained"]
            tmp = self._clean_empty_values_(tmp, cols, "INT")

            for col in cols:
                tmp[col] = locale.atoi(tmp[col])

            result.append(tmp)

        return result, district, stop_loop


    def extract_mucormycosis_info(self, tables):
        df_table = None
        keywords = ["lama", "treatment", "cured", "deaths", "reported"]
        df_table = common_utils.find_table_by_keywords(tables, keywords)

        if df_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(df_table, key_idx=1, val_idx=2)

        keymap = {
            'new_cases': ["day", "new", "cases"],
            'deaths_today': ["day", "new", "deaths"],
            'cured_today': ["day", "cured"],
            'cases_total': ["total", "cases", "reported"],
            'cases_belonging_punjab': ["3.1", "cases", "belonging", "punjab"],
            'cases_belonging_other_states': ["3.2", "cases", "other","states"],
            'under_treatment_total': ["cases", "under", "treatment"],
            'under_treatment_belonging_punjab': ["4.1", "cases", "belonging", "punjab"],
            'under_treatment_beloging_other_states': ["4.2", "cases", "other", "states"],
            'cured_total': ["cured", "till", "date"],
            'cured_total_belonging_punjab': ["5.1", "cases", "belonging", "punjab"],
            'cured_total_belonging_other_states': ["5.2", "cases", "other", "states"],
            'deaths_total': ["deaths", "reported", "till", "date"],
            'deaths_total_belonging_punjab': ["deaths", "belonging", "punjab"],
            'deaths_total_belonging_other_states': ["deaths", "other", "states"],
            'lama': ["lama", "cases"],
            'lama_belonging_punjab': ["lama", "belonging", "punjab"],
            'lama_belonging_other_states': ["lama", "other", "states"]
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        # clean the data
        cols = keymap.keys()
        result = self._clean_empty_values_(result, cols, "INT")
        result = self._clear_extra_char_(result, cols)

        for col in cols:
            if col in result:
                result[col] = locale.atoi(result[col])

        return result

    def extract_mucormycosis_district_info(self, tables):
        df_district = None
        keywords = ["no.", "cases", "day", "reported", "deaths", "till", "date", "under", "treatment"]
        df_district = common_utils.find_table_by_keywords(tables, keywords)
        district_data = dict()
        district_total_key = ""
        cols_in = list()
        result = None

        if df_district is not None:
            df_district = df_district.iloc[1:]
            result = list()
            for i, row in df_district.iterrows():
                row = [x for x in list(row) if x]

                district = row[0].strip().lower()
                if "total" in district:
                    district_total_key = district

                reported_today = row[1].strip() if len(row) > 1 else "0"
                deaths_today = row[2].strip() if len(row) > 2 else "0"
                total_cases = row[3].strip() if len(row) > 3 else "0"
                total_deaths = row[4].strip() if len(row) > 4 else "0"
                total_treatment = row[5].strip() if len(row) > 5 else "0"
                total_cured = row[6].strip() if len(row) > 6 else "0"

                tmp = {
                    "date": self.date,
                    "district": district,
                    "cases_today": reported_today,
                    "deaths_today": deaths_today,
                    "cases_total": total_cases,
                    "deaths_total": total_deaths,
                    "under_treatment": total_treatment,
                    "cured_total": total_cured
                }

                cols = ["cases_today", "deaths_today", "cases_total", "deaths_total", "under_treatment", "cured_total"]
                # clean the data
                tmp = self._clean_empty_values_(tmp, cols, "INT")
                tmp = self._clear_extra_char_(tmp, cols)

                for col in cols:
                    if col in tmp:
                        tmp[col] = locale.atoi(tmp[col])

                result.append(tmp)

        return result


    def extract_mucormycosis_out_state_info(self, tables):
        # parsing second table
        df_out_state = None
        keywords = ["count", "patient", "name", "deaths"]
        df_out_state = common_utils.find_table_by_keywords(tables, keywords)
        result = None

        if df_out_state is not None:
            df_out_state = df_out_state.iloc[1:]
            result = list()
            for i, row in df_out_state.iterrows():
                row = [x for x in list(row) if x]

                city = row[0].strip().lower()
                patients = row[1].strip() if len(row) > 1 else "0"
                deaths = row[2].strip() if len(row) > 2 else "0"

                tmp = {
                    "date": self.date,
                    "city": city,
                    "patients": patients,
                    "deaths": deaths
                }

                cols = ["patients", "deaths"]

                tmp = self._clean_empty_values_(tmp, cols, "INT")
                tmp = self._clear_extra_char_(tmp, cols)
                for col in cols:
                    if col in tmp:
                        tmp[col] = locale.atoi(tmp[col])

                result.append(tmp)

        return result

    def extract(self):
        n = common_utils.n_pages_in_pdf(self.report_fpath) 
        tables = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        case_vaccination_info = self.extract_cases_info(tables)
        patients_info = self.extract_patient_info(tables)
        district_info = self.extract_district_info(tables)
        micro_containment_info = self.extract_micro_containment_zone_info(tables)
        large_containment_info = self.extract_large_containment_zone_info(tables)
        muco_info = self.extract_mucormycosis_info(tables)
        muco_district_info = self.extract_mucormycosis_district_info(tables)
        muco_out_of_state_info = self.extract_mucormycosis_out_state_info(tables)

        result = {
            'cases_vaccination_details': case_vaccination_info,
            'patient_details': patients_info,
            'district_details': district_info,
            'micro_containment_details': micro_containment_info,
            'containment_details': large_containment_info,
            'mucormycorsis_details': muco_info,
            'mucormycorsis_district_details': muco_district_info,
            'mucormycosis_out_state_city_details': muco_out_of_state_info
        }

        return result
        
if __name__ == '__main__':
    date = '24-jul-2021'
    path = "../../../downloads/bulletins/PB/PB-Bulletin-2021-07-20.pdf"
    obj = PunjabExtractor(date, path)
    print(obj.extract())
