from .bulletin import Bulletin

from bs4 import BeautifulSoup
from dateutil import parser

import re

class MadhyaPradesh(Bulletin):

    def __init__(self, basedir):

        statename = 'MP'
        super().__init__(basedir, statename)


    def get_bulletin_links(self):

        burl = "http://sarthak.nhmmp.gov.in/covid/health-bulletin"
        html = self.get_url_html(burl)
        soup = BeautifulSoup(html, 'html.parser')

        bulletin_links = dict()

        for anchor in soup.find_all('a'):

            anchor_href = anchor.get('href')

            if anchor_href:

                match = re.search(r'(\d+.\d+.202\d+)', anchor_href)

                if match:

                    date_time_str = match.group(1)

                    date_time_str = date_time_str.replace("_", ".")
                    date_time_str = date_time_str.replace("202020", "2020")

                    if len(date_time_str) == 8:
                        date_time_str = "{}.{}.{}".format(date_time_str[:2], date_time_str[2:4], date_time_str[4:])

                    try:

                        date_time_obj = parser.parse(date_time_str)
                        datestr = self.get_date_str(str(date_time_obj))

                        bulletin_links[datestr] = anchor_href

                    except: pass

        return bulletin_links


    def run(self):

        print(f'\t Downloading Madhya Pradesh bulletins')

        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links

