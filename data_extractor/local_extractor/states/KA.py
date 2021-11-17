import locale
import dateparser

from camelot.utils import split_textline
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


try:
    from local_extractor.utils import common_utils
    from local_extractor.utils.table_concatenation import concatenate_tables
    from local_extractor.states.state_utils import KA_utils
except ImportError:
    import sys
    import os
    import pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    
    from utils import common_utils
    from utils.table_concatenation import concatenate_tables
    from state_utils import KA_utils


class KarnatakaExtractor(object):
    def __init__(self, date, report_fpath):
        super().__init__()
        self.date = date
        self.report_fpath = report_fpath

    def _get_term_and_value(self, series):
        term_before_value = {
            'Today’s Discharges': 'discharged_new',
            'Total Discharges': 'discharged_total',
            'New Cases Reported': 'cases_new',
            'Total Active Cases': 'cases_active',
            'New Covid Deaths': 'deaths_new',
            'Total Covid Deaths': 'deaths_total',
            'Total Positive Cases': 'cases_total',
            'Positivity rate for the day': 'positivity_rate_percent',
            'Case fatality rate': 'fatality_rate_percent',
            'Admitted in ICU': 'active_cases_icu'
        }
        detected_term = None
        detected_value = None
        for it in series:
            for k, v in term_before_value.items():
                if k in it:
                    detected_term = v
                raw_string = it.strip()
                if raw_string.isdigit():
                    detected_value = int(raw_string)
                elif '%' in raw_string:
                    try:
                        detected_value = float(raw_string[:-1])
                    except:
                        pass
        if detected_term is not None and detected_value is not None:
            return (detected_term, detected_value)
        return (None, None)

    def extract_case_info(self, tables):
        
        if tables is None:
            return None

        keywords = {'active', 'case', 'discharge', 'positive'}
        table = common_utils.find_table_by_keywords(tables, keywords)
        if table is None:
            return None

        df_dict = {}
        for i, row in table.iterrows():
            term, value = self._get_term_and_value(row.values)
            if term is not None:
                df_dict[term] = value
        df_dict['date'] = self.date

        return df_dict

    def find_table_with_text(self, tables, text_to_find):
        for t in tables:
            for row in t.data:
                for col in row:
                    if (text_to_find in col):
                        return t
        return None

    def extract_district_case_information(self, tables):
        if tables is None:
            return None
            
        keywords = {'district', 'wise', 'abstract'}
        table = common_utils.find_table_by_keywords(tables, keywords)
        if table is None:
            return None

        result = []
        for i, row in table.iterrows():
            squished_text = ''.join(row).strip()
            # The first 2 rows are blank. The third row is the table title. The fourth row
            # has the column headers. The last two rows have the totals and maybe some footnote.
            if (
                    len(squished_text) < 2 or
                    squished_text.startswith('Districtwise Abstract') or
                    squished_text.startswith('Total') or
                    squished_text.startswith('Sl.') or
                    squished_text.startswith('*')):
                continue

            colorder = [
                'district', 'cases_new', 'cases_total', 'discharged_new', 'discharged_total', 
                'active_cases_total', 'deaths_new', 'deaths_total', 'non_covid_deaths'
            ]

            tmp = {'date': self.date}

            for idx, colval in enumerate(colorder):
                if row[idx + 1] is None or not row[idx+1].strip():
                    continue
                if colval == 'district':
                    tmp[colval] = row[idx+1].strip().lower()
                else:
                    tmp[colval] = locale.atoi(row[idx+1])

            result.append(tmp)
        return result

    
    def extract_individual_fatalities_data(self, tables):

        keywords = {'dod', 'doa', 'symptom', 'morbidities'}
        datatable = common_utils.find_table_by_keywords(tables, keywords)

        if datatable is None:
            return None

        result = KA_utils.process_individual_fatality_info(datatable)

        for row in result:

            if row['district_name']:
                row['district_name'] = common_utils.clean_numbers_str(row['district_name'])

            if row['age']:
                row['age'] = locale.atoi(common_utils.clean_numbers_str(row['age']))

            if row['doa']:
                try:
                    date = dateparser.parse(row['doa'], ['%d-%m-%Y'])
                    row['doa'] = f'{date.year}-{date.month:02d}-{date.day:02d}'
                except:
                    pass

            if row['dod']:
                try:
                    date = dateparser.parse(row['dod'], ['%d-%m-%Y'])
                    row['dod'] = f'{date.year}-{date.month:02d}-{date.day:02d}'
                except:
                    pass


        return result
        

    def extract(self):
        n = common_utils.n_pages_in_pdf(self.report_fpath)

        # karnataka has one table per page, and each table inside it has
        # a complex system of text and tables embedded in it.

        # First, we get the overall case numbers from the first page.
        # This has to be done without smart boundary detection.
        tables_page0 = common_utils.get_tables_from_pdf(library='camelot',
                                                        pdf_fpath=self.report_fpath,
                                                        smart_boundary_detection=False,
                                                        pages=[1])
        case_info = self.extract_case_info(tables_page0)

        # Then, we get the district-wise numbers. This needs smart boundary detection.
        # Since bulletins have this on different pages, we extract tables from multiple pages
        tables_page4 = common_utils.get_tables_from_pdf(library='camelot',
                                                        pdf_fpath=self.report_fpath,
                                                        smart_boundary_detection=True,
                                                        pages=[2, 3, 4, 5], split_text=False)  
        
        districtwise_info = self.extract_district_case_information(tables_page4)

        # Here, we get all individual fatalities data
        tables_all = common_utils.get_tables_from_pdf(library='camelot', 
                                                        pdf_fpath=self.report_fpath, 
                                                        split_text=False)
        tables_concatenated = concatenate_tables.concatenate_tables(tables_all, heuristic='same-table-width')

        individual_fatality_info = self.extract_individual_fatalities_data(tables_concatenated)


        result = {
            'case-info': case_info,
            'district-cases': districtwise_info,
            'individual-fatalities': individual_fatality_info
        }

        return result


if __name__ == '__main__':
    import os
    date = '08-oct-2021'
    path = os.getenv("HOME") + \
        '/covlocal/bulletins/KA/KA-Bulletin-2021-10-12.pdf'
    obj = KarnatakaExtractor(date, path)
    print(obj.extract())
