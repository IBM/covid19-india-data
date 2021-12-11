import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import pdfplumber
import re
import pandas as pd

try:
    from local_extractor.states.state_utils import TN_utils
except ImportError:

    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor', 'states')
    if path not in sys.path:
        sys.path.insert(0, path)
    from state_utils import TN_utils

try:
    from local_extractor.utils import common_utils
except ImportError:

    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class TamilNaduExtractor(object):
    def __init__(self, date, report_fpath):
        self.date = date
        self.report_fpath = report_fpath
        self.case_parser = TN_utils.read_file

        # for matching facilities string -- example 269 (69 Govt+200 Private)
        self.facilities_nums_regex = re.compile(r'([\d,]+)[ ]*[\(]*([\d,]+)[ ]*([\D]+)[ ]*([\d,]+)[ ]*([\D]+)[\)]*')

    def _parse_facilities_num_(self, data, col, new_cols):
        parsing_successful = False
        if col in data:
            parsed = self.facilities_nums_regex.match(data[col])
            if parsed:
                grps = parsed.groups()
                for new_col in new_cols:
                    # find the relevant index dynamically
                    # what if the government facilities are written at the end
                    if "government" in new_col:
                        for index, s in enumerate(grps):
                            if "Govt" in s:
                                data[new_col] = grps[index - 1]
                                break
                    elif "private" in new_col:
                        for index, s in enumerate(grps):
                            if "Private" in s:
                                data[new_col] = grps[index - 1]
                                break

                data[col] = grps[0]
                parsing_successful = True

        if parsing_successful:
            new_cols.append(col)
            for column in new_cols:
                if ")" in data[column]:
                    data[column] = data[column].replace(")", "")

        return data, parsing_successful

    def _parse_num_(self, data, col, new_cols):
        """
        this parses string like "### / ###", takes data from col and saves it
        in order to new_cols.
        """
        delimeter = "/"
        parsing_successful = False
        #print(data[col])
        if col in data and delimeter in data[col]:
            numbers = data[col].split(delimeter)
            for index, num in enumerate(numbers):
                if num != "":
                    data[new_cols[index]] = num.strip()

            parsing_successful = True

        if parsing_successful:
            for column in new_cols:
                if ")" in data[column]:
                    data[column] = data[column].replace(")", "")

        return data, parsing_successful

    def extract_case_info(self, tables):
        caseinfo_table = None
        # there is only one table in this page
        # checking just to be sure
        if len(tables) == 1:
            caseinfo_table = tables[0].df
        else:
            keywords = {'testing', 'facilities', 'active', 'tested', 'positive', 'deaths', 'discharged', 'following', 'treatment'}
            caseinfo_table = common_utils.find_table_by_keywords(tables, keywords)

        # in case no such table found
        if caseinfo_table is None:
            return None

        df_dict = common_utils.convert_df_to_dict(caseinfo_table, key_idx=1, val_idx=2)
        keymap = {
            "testing_facilities" : ["testing", "facilities"],
            "active_cases_yesterday" : ["active", "till", "yesterday"],
            "positive_tested_cases" : ["tested", "positive"],
            "discharged_patients" : ["discharged", "treatment"],
            "deaths_today" : ["deaths"],
            "active_cases_today" : ["active", "today"]
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        result['date'] = self.date

        # cleaning up numbers
        new_cols =  ["government_testing_facilities", "private_testing_facilities"] 
        result, parsing_successful = self._parse_facilities_num_(result, "testing_facilities", new_cols)

        atoi_cols = list(dict.keys(keymap))
        # if parsing wasnt successful, do not append the new columns
        if parsing_successful:
            atoi_cols.extend(new_cols)

        for col in atoi_cols:
            if isinstance(result[col], int):
                continue

            result[col] = locale.atoi(result[col])

        return result

    def extract_detailed_cases(self, tables):
        # detailed_info_table = None
        # if len(tables) == 1:
        #     detailed_info_table = tables[0].df
        # else:
        keywords = {'positive', 'deaths', 'rt-pcr', 'isolation', 'transgender', 'male', 'female'}
        detailed_info_table = common_utils.find_table_by_keywords(tables, keywords)

        #print(detailed_info_table.size, detailed_info_table.shape)
        # in case no such table found
        # if detailed_info_table is None:
        #     return None

        for table in tables:
            print(table.df)


        df_dict = common_utils.convert_df_to_dict(detailed_info_table, key_idx=1, val_idx=2)
        df_dict = common_utils.add_values_from_neighbors(detailed_info_table, df_dict, key_idx=1, val_idx=2)

        keymap = {
            "total_active_cases": ["active", "including", "isolation"],
            "tested_positive_today": ["persons", "tested", "positive", "tamil"],
            "returned_road_positive_today": ["passengers", "returned", "other", "states", "road"],
            "total_tested_positive": ["persons", "tested", "positive", "till"],
            "rt_pcr_today": ["rt-pcr", "samples"],
            "persons_tested_rt_pcr_today": ["persons", "rt-pcr", "tested"],
            "male_positive_tests": ["male", "transgender", "positive", "today"],
            "total_male_positive_tests": ["male", "transgender", "positive", "till"],
            "discharged_today": ["positive", "patients", "discharged", "following"],
            "total_discharged": ["treatment", "today", "till"],
            "deaths_today": ["deaths", "today", "till"]
        }

        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)
        # copying a specific case which is not being copied
        result['date'] = self.date

        # cleaning up numbers
        atoi_cols = list(dict.keys(keymap))
        atoi_cols.remove("returned_road_positive_today")

        # first rtcpr samples tested row 4
        new_cols = ["rt_pcr_today", "total_rt_pcr"]
        result, parsing_successful = self._parse_num_(result, "rt_pcr_today", new_cols)
        if parsing_successful:
            atoi_cols.append(new_cols[1])

            if "@" in result["total_rt_pcr"]:
                result["total_rt_pcr"] = result["total_rt_pcr"].replace("@", "")

        # rtpcr persons tested row 5
        new_cols = ["persons_tested_rt_pcr_today", "total_persons_tested_rt_pcr"]
        result, parsing_successful = self._parse_num_(result, new_cols[0], new_cols)
        if parsing_successful: atoi_cols.append(new_cols[1])

        # gender tested positive today row 6
        new_cols = ["male_positive_tests", "female_positive_tests", "transgender_positive_tests"]
        result, parsing_successful = self._parse_num_(result, new_cols[0], new_cols)
        if parsing_successful: atoi_cols.extend([new_cols[1], new_cols[2]])

        # gender tested positive till date row 7
        new_cols = ["total_male_positive_tests", "total_female_positive_tests", "total_transgender_positive_tests"]
        result, parsing_successful = self._parse_num_(result, new_cols[0], new_cols)
        if parsing_successful: atoi_cols.extend([new_cols[1], new_cols[2]])

        # discharged numbers row 9
        new_cols = ["discharged_today", "total_discharged"]
        result, parsing_successful = self._parse_num_(result, new_cols[0], new_cols)
        if parsing_successful: atoi_cols.append(new_cols[1])

        # deaths row 10
        new_cols = ["deaths_today", "total_deaths"]
        result, parsing_successful = self._parse_num_(result, new_cols[0], new_cols)
        if parsing_successful: atoi_cols.append(new_cols[1])

        new_cols = ["deaths_government_hopitals", "deaths_private_hospitals"]
        result, parsing_succesful = self._parse_facilities_num_(result, "deaths_today", new_cols)
        if parsing_successful: atoi_cols.extend(new_cols)

        # converting from strings to numbers
        for col in atoi_cols:
            if isinstance(result[col], int):
                continue

            result[col] = locale.atoi(result[col])

        return result

    def extract_district_cases(self, district_tables, is_page5_present=False):
        df_page3 = None
        df_page4 = None
        df_page6 = None
        keywords_page3 = ["home",  "death", "treatment", "discharged"]
        df_page3 = common_utils.find_table_by_keywords(district_tables, keywords_page3)

        keywords_page4 = ["indigenous", "imported"]
        df_page4 = common_utils.find_table_by_keywords(district_tables, keywords_page4)

        keywords_page6 = ["positive", "discharged", "active", "death"]
        df_page6 = common_utils.find_table_by_keywords(district_tables, keywords_page6)

        result = []
        district_numbers = dict()
        stop_loop = False

        # parsing table 3
        if df_page3 is not None:
            df_page3 = df_page3.iloc[1:]
            for i, row in df_page3.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if row[0].strip().lower() == 'grand total':
                    counter = 0
                    stop_loop = True
                else:
                    counter = 1

                district = row[0 + counter].strip().lower()

                active_cases_till_yesterday = row[1 + counter].strip()
                new_cases_today = row[2 + counter].strip()
                discharged_cases_today = row[3 + counter].strip()
                deaths_today = row[4 + counter].strip()
                total_active_cases = row[5 + counter].strip()

                tmp = {
                    'date': self.date,
                    "district": district,
                    "total_active_cases_till_yesterday": active_cases_till_yesterday,
                    "new_cases_today": new_cases_today,
                    "discharged_cases_today": discharged_cases_today,
                    "deaths_today": deaths_today,
                    "total_active_cases_including_today": total_active_cases,
                }

                district_numbers[district] = tmp

        stop_loop = False
        if df_page4 is not None:
            df_page4 = df_page4.iloc[2:]
            for i, row in df_page4.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if row[0].strip().lower() == 'grand total':
                    counter = 0
                    stop_loop = True
                else:
                    counter = 1

                district = row[0 + counter].strip().lower()
                indegenous_cases_yesterday = row[1 + counter].strip()
                indegenous_cases_today = row[2 + counter].strip()
                imported_cases_yesterday = row[3 + counter].strip()
                imported_cases_today = row[4 + counter].strip()
                total_cases_today = row[5 + counter].strip()
                tmp = {
                    'total_indegenous_cases_till_yesterday': indegenous_cases_yesterday,
                    'indegenous_cases_today': indegenous_cases_today,
                    'total_imported_cases_till_yesterday': imported_cases_yesterday,
                    'imported_cases_today': imported_cases_today,
                    'total_cases_till_today': total_cases_today
                }

                if district in district_numbers:
                    district_numbers[district].update(tmp)
                else:
                    # this should never happen but in case there is an error
                    print("district not found page 4", district)
                    tmp['district'] = district
                    tmp['date'] = self.date
                    distrct_numbers[district] = tmp

        stop_loop = False
        if df_page6 is not None:
            df_page6 = df_page6.iloc[1:]
            for i, row in df_page6.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if row[0].strip().lower() == 'grand total':
                    counter = 0
                    stop_loop = True
                else:
                    counter = 1

                district = row[0 + counter].strip().lower()
                total_discharged = row[2 + counter].strip()
                total_deaths = row[4 + counter].strip()

                tmp = {
                    'total_cases_discharged': total_discharged,
                    'total_deaths': total_deaths
                }

                if district in district_numbers:
                    district_numbers[district].update(tmp)
                else:
                    # this should never happen in case there is an error
                    print("district not found page 6", district)
                    tmp['district'] = district
                    tmp['date'] = self.date
                    district_numbers[district] = tmp

        for k, v in district_numbers.items():
            for key, value in v.items():
                if key == "district" or key == "date":
                    continue

                v[key] = locale.atoi(value)

        # converting district wise dictionary to a list of rows
        for _, v in district_numbers.items():
            result.append(v)

        return result


    def extract_district_facilities_details(self, district_tables):
        df_page7 = None
        df_page8 = None
        df_page9 = None
        keywords_page7 = ["o2", "occupancy", "vacancy", "earmarked", "icu"]
        df_page7 = common_utils.find_table_by_keywords(district_tables, keywords_page7)

        keywords_page8 = ["ccc"]
        df_page8 = common_utils.find_table_by_keywords(district_tables, keywords_page8)

        keywords_page9 = ["urban", "rural", ]
        df_page9 = common_utils.find_table_by_keywords(district_tables, keywords_page9)

        result = []
        district_numbers = dict()
        stop_loop = False

        # parsing table 3
        if df_page7 is not None:
            df_page7 = df_page7.iloc[3:]
            for i, row in df_page7.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if row[0].strip().lower() == 'grand total':
                    counter = 0
                    stop_loop = True
                else:
                    counter = 1

                district = row[0 + counter].strip().lower()

                covid_o2 = row[1 + counter].strip()
                covid_non_o2 = row[2 + counter].strip()
                covid_icu = row[3 + counter].strip()
                occupancy_o2 = row[4 + counter].strip()
                occupancy_non_o2 = row[5 + counter].strip()
                occupancy_icu = row[6 + counter].strip()
                vacancy_o2 = row[7 + counter].strip()
                vacancy_non_o2 = row[8 + counter].strip()
                vacancy_icu = row[9 + counter].strip()
                total_vacancy = row[10 + counter].strip()

                tmp = {
                    'date': self.date,
                    "district": district,
                    'total_covid_o2': covid_o2,
                    'total_covid_non_o2': covid_non_o2,
                    'total_covid_icu': covid_icu,
                    'today_occupancy_o2': occupancy_o2,
                    'today_occupancy_non_o2': occupancy_non_o2,
                    'today_occupancy_icu': occupancy_icu,
                    'total_vacancy_o2': vacancy_o2,
                    'total_vacancy_non_o2': vacancy_non_o2,
                    'total_vacancy_icu': vacancy_icu,
                    'total_vacancy': total_vacancy
                }

                district_numbers[district] = tmp

        stop_loop = False
        if df_page8 is not None:
            df_page8 = df_page8.iloc[2:]
            for i, row in df_page8.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if row[0].strip().lower() == 'grand total':
                    counter = 0
                    stop_loop = True
                else:
                    counter = 1

                district = row[0 + counter].strip().lower()
                embarked_covid = row[1 + counter].strip()
                embarked_occupancy = row[2 + counter].strip()
                embarked_vacancy = row[3 + counter].strip()
                tmp = {
                    'embarked_covid_beds': embarked_covid,
                    'embarked_covid_occupancy': embarked_occupancy,
                    'embarked_covid_vacancy': embarked_vacancy
                }

                if district in district_numbers:
                    district_numbers[district].update(tmp)
                else:
                    # this should never happen but in case there is an error
                    print("district not found page 8", district)
                    tmp['district'] = district
                    tmp['date'] = self.date
                    district_numbers[district] = tmp

        stop_loop = False
        if df_page9 is not None:
            df_page9 = df_page9.iloc[3:]
            for i, row in df_page9.iterrows():
                if stop_loop:
                    break

                row = [x for x in list(row) if x]

                if row[0].strip().lower() == 'total':
                    counter = 0
                    stop_loop = True
                    # for some reason here they write total at the end :facepalm
                    district = "grand total"
                else:
                    counter = 1
                    district = row[0 + counter].strip().lower()

                proposed_rural = row[1 + counter].strip()
                beds_proposed_rural = row[2 + counter].strip()
                beds_available_rural = row[3 + counter].strip()
                beds_occupied_rural = row[4 + counter].strip()
                proposed_urban = row[5 + counter].strip()
                beds_urban = row[6 + counter].strip()

                tmp = {
                    'iccc_proposed_rural': proposed_rural,
                    'iccc_beds_proposed_rural': beds_proposed_rural,
                    'iccc_total_beds_available_rural': beds_available_rural,
                    'iccc_beds_occupied_rural': beds_occupied_rural,
                    'iccc_proposed_urban': proposed_urban,
                    'iccc_beds_proposed_urban': beds_urban
                }

                if district in district_numbers:
                    district_numbers[district].update(tmp)
                else:
                    # this should never happen in case there is an error
                    print("district not found page 9", district)
                    tmp['district'] = district
                    tmp['date'] = self.date
                    district_numbers[district] = tmp

        for k, v in district_numbers.items():
            for key, value in v.items():
                if key == "district" or key == "date":
                    continue

                if "#" in value:
                    value = value.replace('#', '')

                v[key] = locale.atoi(value)

        # converting district wise dictionary to a list of rows
        for _, v in district_numbers.items():
            result.append(v)

        return result

    def extract_death_comorbidities_table(self, death_detail_tables):
        df_page10a = None
        df_page10b = None
        keywords = ["no", "comorbidities"]
        df_page10a = common_utils.find_table_by_keywords(death_detail_tables, keywords)

        keywords = ["with", "comorbidities"]
        df_page10b = common_utils.find_table_by_keywords(death_detail_tables, keywords)

        if df_page10a is None and df_page10b is None:
            return None

        keymap_no_comorbidities = {
            "no_comorbidities_government_dme": ["government", "dme"],
            "no_comorbidities_government_dms": ["government", "dms"],
            "no_comorbidities_private": ["private"],
            "no_comorbidities_other_government": ["other", "railway", "government", "institutions"],
            "no_comorbidities_total": ["total"]
        }

        keymap_comorbidities = {
            "comorbidities_government_dme": ["government", "dme"],
            "comorbidities_government_dms": ["government", "dms"],
            "comorbidities_private": ["private"],
            "comorbidities_other_government": ["other", "railway", "government", "institutions"],
            "comorbidities_total": ["total"]
        }

        if df_page10a is not None:
            df_dict_page10a = common_utils.convert_df_to_dict(df_page10a, key_idx=0, val_idx=1)
            result = common_utils.extract_info_from_table_by_keywords(df_dict_page10a, keymap_no_comorbidities)

        if df_page10b is not None:
            df_dict_page10b = common_utils.convert_df_to_dict(df_page10b, key_idx=0, val_idx=1)
            tmp = common_utils.extract_info_from_table_by_keywords(df_dict_page10b, keymap_comorbidities)

        if df_page10a is None:
            result = tmp
        elif df_page10b is None:
            result = result
        else:
            result.update(tmp)

        result['date'] = self.date

        cols = list(result.keys())
        for col in cols:
            if col == "date":
                continue

            result[col] = locale.atoi(result[col])

        return result

    def extract_travel_mode_table(self, travel_info_tables):
        df = None
        keywords = ["mode", "travel", "since"]
        df = common_utils.find_table_by_keywords(travel_info_tables, keywords)

        if df is None:
            return None

        stop_loop = False
        result = list()
        df = df.iloc[1:]
        for i, row in df.iterrows():
            if stop_loop:
                break

            row = [x for x in list(row) if x]

            if row[0].strip().lower() == 'total':
                counter = 0
                stop_loop = True
                # keeping the same name for total in case something comes up
                # later
                travel_mode = "grand total"
            else:
                counter = 1
                travel_mode = row[1].strip().lower()

            passengers = row[1 + counter].strip()

            tmp = {
                'travel_mode': travel_mode,
                'passengers': passengers,
            }

            if len(row) == 3 + counter:
                tmp['positive_cases'] = row[2 + counter].strip()

            tmp['date'] = self.date
            result.append(tmp)

        for mode in result:
            for key, value in mode.items():
                if key == "date" or key == "travel_mode":
                    continue

                mode[key] = locale.atoi(value)

        return result

    def extract_airport_surveillance_table(self, travel_info_tables):
        df = None
        keywords = ["flights", "arrived", "passengers"]
        df = common_utils.find_table_by_keywords(travel_info_tables, keywords)

        if df is None:
            return None

        stop_loop = False
        result = list()
        df = df.iloc[1:]
        for i, row in df.iterrows():
            if stop_loop:
                break

            row = [x for x in list(row) if x]

            if row[0].strip().lower() == 'total':
                counter = 0
                stop_loop = True
                # keeping the same name for total in case something comes up
                # later
                airport = "grand total"
            else:
                counter = 1
                airport = row[1].strip().lower()

            flights = row[1 + counter].strip()
            passengers = row[2 + counter].strip()
            positive = row[3 + counter].strip()
            tmp = {
                'airport': airport,
                'flights_arrived': flights,
                'passengers': passengers,
                'positive_cases': positive
            }

            tmp['date'] = self.date
            result.append(tmp)

        for airport in result:
            for key, value in airport.items():
                if key == "date" or key == "airport":
                    continue

                airport[key] = locale.atoi(value)

        return result

    def extract_airport_flight_table(self, travel_info_tables):
        # this table is across 3 pages, it usually starts on one page with only 2
        # rows. 3rd page table might not be there, so I have an extra check for it.
        df_header = None
        df_body = None
        df_footer = None

        keywords_header = ["airport", "total", "process"]
        df_header = common_utils.find_table_by_keywords(travel_info_tables, keywords_header)

        keywords_body = ["coimbatore", "madurai", "from", "sub"]
        df_body = common_utils.find_table_by_keywords(travel_info_tables, keywords_body)

        keywords_footer = ["chartered", "other"]
        df_footer = common_utils.find_table_by_keywords(travel_info_tables, keywords_footer)

        if df_header is None and df_body is None and df_footer is None:
            return None

        result = list()
        # setting it to a value as it is not supposed to be null in the table
        airport = "chennai"

        # no header means there is no table as that has the column names
        if df_header is None:
            return None

        stop_loop = False
        df_header = df_header.iloc[2:]
        for i, row in df_header.iterrows():
            if stop_loop:
                break

            row = [x for x in list(row) if x]
            if len(row) == 1:
                airport = self._get_airport(row)
                continue

            tmp = self._get_flight_detail(row)
            tmp['airport'] = airport

            result.append(tmp)

        if df_body is not None:
            for i, row in df_body.iterrows():
                row = [x for x in list(row) if x]
                if len(row) == 1:
                    airport = self._get_airport(row)
                    continue

                tmp = self._get_flight_detail(row)
                if 'airport' not in tmp:
                    tmp['airport'] = airport

                result.append(tmp)

        # this ensures that the footer data is new and no same
        # rows are being parsed
        if df_footer is not None and df_body is not None and df_body.size != df_footer.size:
            for i, row in df_footer.iterrows():
                row = [x for x in list(row) if x]
                if len(row) == 1:
                    airport = self._get_airport(row)
                    continue

                tmp = self._get_flight_detail(row, 0)
                # assumption is that after other the only row left is grand total
                if 'airport' not in tmp:
                    tmp['airport'] = airport

                result.append(tmp)

        for row in result:
            for k, v in row.items():
                if k == "date" or k == "flight" or k == "airport":
                    continue

                row[k] = locale.atoi(v)

        return result

    def _get_airport(self, row):
        airport = row[0].strip().lower()
        # matching the name to the other table
        if "airport" in airport:
            airport = airport.replace(" airport", "")

        return airport

    def _get_flight_detail(self, row, counter_other = 1):
        if "other" in row[0].strip().lower():
            if len(row) == 3:
                tmp = {
                    "airport": "other",
                    "flight": row[0].strip().lower(),
                    # "positive_during_entry_screening": row[1 + counter_other].strip(),
                    # "positive_during_exit_screening": row[2 + counter_other].strip()
                    "positive_during_entry_screening": row[1].strip(),
                    "positive_during_exit_screening": row[2].strip()
                }
            else:
                tmp = {
                    "airport": "other",
                    "flight": row[0].strip().lower(),
                    "total_passengers": row[1 + counter_other].strip(),
                    "passengers_tested": row[2 + counter_other].strip(),
                    "tests_under_process": row[3 + counter_other].strip(),
                    "negative": row[4 + counter_other].strip(),
                    "positive_during_entry_screening": row[5 + counter_other].strip(),
                    "positive_during_exit_screening": row[6 + counter_other].strip()
                }
            tmp['date'] = self.date

            return tmp

        if 'total' in row[0].strip().lower() or "/" in row[0].strip():
            counter = 0
        else:
            counter = 1

        flight = row[0 + counter].strip().lower()
        total = row[1 + counter].strip()
        tested = row[2 + counter].strip()
        under_process = row[3 + counter].strip()
        tmp = {
            "flight": flight,
            "total_passengers": total,
            "passengers_tested": tested,
            "tests_under_process": under_process
        }
        tmp['date'] = self.date

        if len(row) > 5:
            tmp["negative"] = row[4 + counter].strip()

        if len(row) > 6:
            tmp["positive_during_entry_screening"] = row[5 + counter].strip()
        if len(row) > 7:
            tmp["positive_during_exit_screening"] = row[6 + counter].strip()

        # matching airport to the other table
        if flight == "grand total":
            tmp["airport"] = flight

        return tmp


    def extract_train_surveillance_table(self, travel_info_tables):
        df = None
        keywords = ["trains", "negative", "positive"]
        df = common_utils.find_table_by_keywords(travel_info_tables, keywords)

        # null check
        if df is None:
            return None

        df = df.iloc[1:]
        result = list()
        rows = 0
        for i, row in df.iterrows():
            row = [x for x in list(row) if x]

            trains = row[0].strip()
            passengers = row[1].strip()
            negative = row[2].strip()
            positive = row[3].strip()

            tmp = {
                'trains': trains,
                'passengers': passengers,
                'negative_cases': negative,
                'positive_cases': positive
            }
            tmp['date'] = self.date

            rows += 1
            result.append(tmp)

        # usually there is only one row of info in the table
        # just to be cautious we first add the info to list
        # then change the type only if the number of rows is 1
        if rows == 1:
            result = tmp
            for key, value in result.items():
                if key == "date" or key == "trains":
                    continue

                result[key] = locale.atoi(value)
        else:
            for train_info in result:
                for key, value in train_info.items():
                    if key == "date":
                        continue

                    train_info[key] = locale.atoi(value)

        return result

    def extract_seaport_surveillance_table(self, travel_info_tables):
        df = None
        keywords = ["sea", "port", "ships", "arrived"]
        df = common_utils.find_table_by_keywords(travel_info_tables, keywords)

        if df is None:
            return None

        df = df.iloc[1:]
        result = list()
        stop_loop = False
        for i, row in df.iterrows():
            if stop_loop:
                break

            row = [x for x in list(row) if x]

            if row[0].strip().lower() == 'total':
                counter = 0
                stop_loop = True
                # keeping the same name for total in case something comes up
                # later
                seaport = "grand total"
            else:
                counter = 1
                seaport = row[1].strip().lower()

            ships = row[1 + counter].strip()
            passengers = row[2 + counter].strip()
            positive = row[3 + counter].strip()
            tmp = {
                'seaport': seaport,
                'ships_arrived': ships,
                'passengers': passengers,
                'positive_cases': positive
            }

            tmp['date'] = self.date
            result.append(tmp)

        for port in result:
            for key, value in port.items():
                if key == "date" or key == "seaport":
                    continue

                port[key] = locale.atoi(value)

        return result

    def extract_individual_case_info(self):
        return self.case_parser(self.report_fpath)

    def extract(self):
        n = common_utils.n_pages_in_pdf(self.report_fpath)
        #print("number of pages ", n)
        # file consists of a table on page 1 and an advertisement :D
        tables_page1 = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[1])
        # tables_page2 = common_utils.get_tables_from_pdf(library='tabula', pdf_fpath=self.report_fpath, pages=[2], smart_boundary_detection=True)
        # gettting all district case tables
        """
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        """
        tables_district = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[3, 4, 5, 7, 9, 10], use_stream=False)
        tables_comorbidities = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[10], use_stream=False)
        tables_travel_data = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath, pages=[n-2, n-1, n], use_stream=False)

        # send first table to extract the cummulative case details
        cummulative_case_info = self.extract_case_info(tables_page1)
        # detailed_case_info = self.extract_detailed_cases(tables_page2)
        district_cases = self.extract_district_cases(tables_district)
        bed_details = self.extract_district_facilities_details(tables_district)
        death_details = self.extract_death_comorbidities_table(tables_comorbidities)
        travel_mode_details = self.extract_travel_mode_table(tables_travel_data)
        airport_details = self.extract_airport_surveillance_table(tables_travel_data)
        flight_details = self.extract_airport_flight_table(tables_travel_data)
        train_details = self.extract_train_surveillance_table(tables_travel_data)
        seaport_details = self.extract_seaport_surveillance_table(tables_travel_data)

        # TODO: Need to save this
        # individual_case_info = self.extract_individual_case_info()
        # print(individual_case_info)

        result = {
            'case-info': cummulative_case_info,
            # 'detailed-info': detailed_case_info,
            'district-info': district_cases,
            'district-bed-info': bed_details,
            'death-info': death_details,
            'travel-info': travel_mode_details,
            'airport': airport_details,
            'flights': flight_details,
            'trains': train_details,
            'ships': seaport_details
        }

        return result


if __name__ == "__main__":

    # date = "17-sep-2021"
    # path = "../../../downloads/bulletins/TN/TN-Bulletin-2021-09-17.pdf"

    date = "2021-11-07"
    path = "/Users/tchakra2/Desktop/bulletins/Media-Bulletin-07-11-21-COVID-19.pdf"

    date = "2021-09-08"
    path = "/Users/tchakra2/Desktop/bulletins/Media-Bulletin-08-09-21-COVID-19.pdf"

    # date = "2021-11-23"
    # path = "/Users/tchakra2/Desktop/bulletins/Media-Bulletin-23-11-21-COVID-19-1.pdf"

    # date = "2021-12-01"
    # path = "/Users/tchakra2/Desktop/bulletins/Media-Bulletin-01-12-21-COVID-19.pdf"

    reader = TamilNaduExtractor(date, path)

    from pprint import pprint
    pprint(reader.extract())




