from os import link
from .bulletin import Bulletin
from bs4 import BeautifulSoup

import re


class TamilNadu(Bulletin):

    def __init__(self, basedir):

        statename = 'TN'
        super().__init__(basedir, statename)

        self.bulletin_url = 'https://stopcorona.tn.gov.in/daily-bulletin/'
        self.archive_bulletin_url = 'https://stopcorona.tn.gov.in/archive/'
        self.date_regex = re.compile(r'(\d{2})[\.-](\d{2})[\.-](\d{4})')

    def get_bulletin_links(self, url):

        html = self.get_url_html(url)
        html_parsed = BeautifulSoup(html, 'html.parser')
        bulletin_anchors = [
            anchor for anchor in html_parsed.find_all('a')
            if 'bulletin' in anchor.text.lower()
        ]

        link_dict = {}

        for anchor in bulletin_anchors:
            
            try:
                anchor_str = anchor.text.lower().strip()
                anchor_href = anchor['href']

                match = self.date_regex.search(anchor_str)
                day, month, year = match.groups()
                datestr = f'{year}-{month}-{day}'
                datestr = self.get_date_str(datestr)
            except:
                pass
            else:
                link_dict[datestr] = anchor_href

        return link_dict

    def run(self):

        print(f'\t Downloading Tamil Nadu bulletins')

        linkdict1 = self.get_bulletin_links(self.bulletin_url)
        linkdict2 = self.get_bulletin_links(self.archive_bulletin_url)
        
        linkdict1.update(linkdict2)
        bulletin_links = linkdict1

        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links


# tn = TamilNadu("")
# tn_bulletins = tn.run()

# for b in tn_bulletins:
#     print(f"{b} : {tn_bulletins[b]}")


