import dateparser

from .bulletin import Bulletin
from bs4 import BeautifulSoup
from urllib.parse import urljoin


class Karnataka(Bulletin):
    def __init__(self, basedir):
        statename = 'KA'
        super().__init__(basedir, statename)

        self.bulletin_url = 'https://covid19.karnataka.gov.in/govt_bulletin/en'
        self.match_text = 'hmb english.pdf'

    def get_date_str_ka(self, datestr):
        if datestr is None:
          return None
        # KA bulletins use the DD-MM-YYYY format, so we explicitly mention
        # the format here in case the algorithm gets confused between
        # days and months.
        date = dateparser.parse(datestr, ['%d-%m-%Y'])

        if date is None:
            return None

        datestr = f'{date.year}-{date.month:02d}-{date.day:02d}'
        return datestr

    def get_bulletin_links(self):
        html = self.get_url_html(self.bulletin_url)
        html_parsed = BeautifulSoup(html, 'html.parser')

        # All karnataka bulletin links end in 'HMB English.pdf'
        bulletin_anchors = [
            anchor for anchor in html_parsed.find_all('a')
            if anchor.text.lower().strip().endswith(self.match_text)
        ]
        link_dict = {}

        for anchor in bulletin_anchors:
            datestr = anchor.text.lower().split(' ')[0].strip()
            datestr = self.get_date_str_ka(datestr)

            if datestr is None:
                continue

            try:
                # Karnataka links skip the domain name, so we have to join
                href = urljoin(self.bulletin_url, anchor['href'])
            except:
                continue

            link_dict[datestr] = href

        return link_dict

    def run(self):
        print(f'\t Downloading Karnataka bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links

