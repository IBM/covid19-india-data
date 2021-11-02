import locale
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')


try:
    from local_extractor.utils import common_utils
except ImportError:
    import sys
    import os
    import pathlib
    path = pathlib.Path(__file__).absolute().parents[2]
    path = os.path.join(path, 'local_extractor')
    if path not in sys.path:
        sys.path.insert(0, path)
    from utils import common_utils


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
            'Total Active Cases': 'cases_active_new',
            'New Covid Deaths': 'deaths_new',
            'Total Covid Deaths': 'deaths_total',
            'Total Positive Cases': 'cases_active_total',
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

    def extract_case_info(self, table):
        if table is None:
            return None
        df_dict = {}
        for i, row in table.df.iterrows():
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

        table = self.find_table_with_text(tables, 'Districtwise Abstract')
        if table is None:
            return None

        result = []
        for i, row in table.df.iterrows():
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

            tmp = {
                'date': self.date,
                'district': row[1],
                'cases_new': row[2],
                'cases_total': row[3],
                'discharged_new': row[4],
                'discharged_total': row[5],
                'active_cases_total': row[6],
                'deaths_new': row[7],
                'deaths_total': row[8],
                'non_covid_deaths': row[9]
            }
            result.append(tmp)
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
        case_info = self.extract_case_info(tables_page0[0])

        # Then, we get the district-wise numbers. This needs smart boundary detection.
        # Since older bulletins have this table on page 3 while newer bulletins have
        # this on page 4, we extract tables from both pages
        tables_page4 = common_utils.get_tables_from_pdf(library='camelot',
                                                        pdf_fpath=self.report_fpath,
                                                        smart_boundary_detection=True,
                                                        pages=[3, 4])
        districtwise_info = self.extract_district_case_information(
            tables_page4)

        result = {
            'case-info': case_info,
            'district-cases': districtwise_info
        }

        return result


if __name__ == '__main__':
    import os
    date = '08-oct-2021'
    path = os.getenv("HOME") + \
        '/covlocal/bulletins/KA/KA-Bulletin-2021-10-12.pdf'
    obj = KarnatakaExtractor(date, path)
    print(obj.extract())
