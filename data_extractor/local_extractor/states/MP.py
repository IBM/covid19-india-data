import dateparser
import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys, os, pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


class MadhyaPradeshExtractor(object):

    def __init__(self, date, report_fpath):
        super().__init__()

        self.date = date
        self.report_fpath = report_fpath

    def __extract_generic(self, datatable, keymap, major_key, minor_key):

        df_dict = common_utils.convert_df_to_dict(datatable, key_idx=major_key, val_idx=minor_key)
        result = common_utils.extract_info_from_table_by_keywords(df_dict, keymap)

        for key in result.keys():
            try: result[key] = locale.atoi(result[key])
            except: pass

        result['date'] = self.date
        return result

    def __get_date_str(self, datestr):
        date = dateparser.parse(datestr)

        if date is None:
            return None
            
        datestr = f'{date.year}-{date.month:02d}-{date.day:02d}'
        return datestr


    def extract_overview(self, tables):
        # UNABLE TO PARSE HINDI TEXT #
        return None


    def extract_district_info(self, tables):

        def __read_district_subtable(datatable):

            result = list()
            keymapidx = {
                'district': 1,
                'new_positive': 2,
                'cumulative_positive': 3,
                'new_deaths': 4,
                'cumulative_deaths': 5,
                'new_recovered': 6,
                'cumulative_recovered': 7,
                'active_cases': 8
            }

            for index, row in datatable.iterrows():
                new_result = {
                    "date" : self.date
                }

                for key in keymapidx:
                    new_result[key] = row[keymapidx[key]]

                    try: new_result[key] = locale.atoi(new_result[key])
                    except: pass

                result.append(new_result)

            return result


        datatable_part_1 = common_utils.find_table_by_keywords(tables, {"bhopal"})
        datatable_foil_part_1 = common_utils.find_table_by_keywords(tables, {"bhopal", "vaccination coverage"})

        result = list()

        if datatable_part_1 is not None:
            if not datatable_part_1.equals(datatable_foil_part_1):

                datatable_part_1 = datatable_part_1.iloc[1:]
                result = __read_district_subtable(datatable_part_1)

        datatable_part_2 = common_utils.find_table_by_keywords(tables, {"total"})
        datatable_foil_part_2 = common_utils.find_table_by_keywords(tables, {"total", "vidisha"})

        new_result = list()

        if datatable_part_2 is not None:
            if not datatable_part_2.equals(datatable_foil_part_2):
                if datatable_part_2.loc[len(datatable_part_2.index)-1,1].strip() == "Total":

                    new_result = __read_district_subtable(datatable_part_2)

        return result + new_result


    def extract_calls(self, tables):

        datatable = common_utils.find_table_by_keywords(tables, {"call type"})

        if datatable is not None:

            keymap = {
                'information': ['information'],
                'medical_advice': ['advise'],
                'counselling': ['counseling'],
                'complaint': ['complaint'],
                'total': ['total'],
            }

            return self.__extract_generic(datatable, keymap, major_key=0, minor_key=1)


    def extract_centers(self, tables):

        datatable = common_utils.find_table_by_keywords(tables, {"total isolation beds", "excluding icu bed"})

        if datatable is not None:

            datatable.loc[4,1] = datatable.loc[4,0]
            datatable = datatable.iloc[1:, 1:]

            result = list()

            for index, row in datatable.iterrows():
                new_result = {
                    "date"                 : self.date,
                    "category"             : row[1],
                    "number_of"            : row[2],
                    "total_isolation_beds" : row[3],
                    "total_icu_beds"       : row[4],
                    "total_beds"           : row[5],
                    "total_ventilators"    : row[6],
                }

                for key in new_result.keys():
                    try: new_result[key] = locale.atoi(new_result[key])
                    except: pass

                result.append(new_result)

            return result


    def extract_teams(self, tables):

        datatable = common_utils.find_table_by_keywords(tables, {"rapid response"})

        if datatable is not None:

            datatable = datatable.transpose()
            keymap = {
                'rrt': ['rapid response', '(rrt)'],
                'srrt': ['rapid response', '(srrt)'],
                'mmu': ['mmu'],
                'phmu': ['phmu'],
                'surveillance': ['surveillance'],
            }

            return self.__extract_generic(datatable, keymap, major_key=0, minor_key=1)


    def extract_testing(self, tables):

        datatable = common_utils.find_table_by_keywords(tables, {"fnukad", "rd"})

        if datatable is not None:

            parse_on = False
            date = None

            result = list()

            for index, row in datatable.iterrows():

                if parse_on: 

                    row = row[0].split()
                    new_result = {
                        'date'             : date,
                        'samples_sent'     : row[0],
                        'reports_received' : row[1],
                        'reports_pending'  : row[2],
                        'positive_report'  : row[3],
                        'negative_report'  : row[4],
                    }

                    for key in new_result.keys():
                        try: new_result[key] = locale.atoi(new_result[key])
                        except: pass

                    result.append(new_result)

                parse_on = "fnukad" in row[0]

                if parse_on:
                    date = self.__get_date_str(row[0].split()[1])

            return result


    def extract_vaccination_coverage(self, tables):

        datatables = [
                common_utils.find_table_by_keywords(tables, {"vaccination coverage"}),
                common_utils.find_table_by_keywords(tables, {"total", "vidisha"})
            ]

        result = list()

        for datatable in datatables:

            if datatable is not None:

                split_tables = [
                    datatable.iloc[3:, :4],
                    datatable.iloc[3:, 4:]
                ]

                for table in split_tables:

                    keys = {
                        "doses_today" : 2,
                        "doses_total" : 3,
                    }

                    new_result = dict()

                    for key in keys:

                        key_idx = 1
                        val_idx = keys[key]

                        df_dict = common_utils.convert_df_to_dict(table, key_idx, val_idx)

                        for item in df_dict:

                            if item in new_result: 
                                new_result[item][key] = df_dict[item]

                            else: 
                                new_result[item] = dict()
                                new_result[item][key] = df_dict[item]

                    for item in new_result:

                        for key in new_result.keys():
                            try: new_result[key] = locale.atoi(new_result[key])
                            except: pass

                        result.append({
                                "date": self.date,
                                "district": item,
                                "doses_today": new_result[item]["doses_today"],
                                "doses_total": new_result[item]["doses_total"],
                            })

        return result


    def extract(self):

        if self.date <= "2020-05-20":
            return dict()

        all_tables_camelot = common_utils.get_tables_from_pdf(library='camelot', pdf_fpath=self.report_fpath)
        result = {
            'overview': self.extract_overview(all_tables_camelot),
            'district-info': self.extract_district_info(all_tables_camelot),
            'calls': self.extract_calls(all_tables_camelot),
            'centers': self.extract_centers(all_tables_camelot),
            'teams': self.extract_teams(all_tables_camelot),
            'testing': self.extract_testing(all_tables_camelot),
            'vaccination-coverage': self.extract_vaccination_coverage(all_tables_camelot),
        }

        return result


if __name__ == '__main__':

    # date = '2020-10-10'
    # path = "/Users/tchakra2/Desktop/bulletins/Letter_Health_Bulletin_25.10.2021_V3-.pdf"

    # date = '2020-09-19'
    # path = "/Users/tchakra2/Desktop/bulletins/Letter-Health-Bulletin-19.09.2020.pdf"

    # date = '2021-01-03'
    # path = "/Users/tchakra2/Desktop/bulletins/Letter-Health-Bulletin-03.01.2021.pdf"

    date = '2020-04-20'
    path = "/Users/tchakra2/Desktop/bulletins/20.4.2020-Health-Bulatin.pdf"

    obj = MadhyaPradeshExtractor(date, path)

    from pprint import pprint
    pprint(obj.extract())

