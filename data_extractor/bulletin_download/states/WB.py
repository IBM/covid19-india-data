from .bulletin import Bulletin
from bs4 import BeautifulSoup


class WestBengal(Bulletin):

    def __init__(self, basedir):

        statename = 'WB'
        super().__init__(basedir, statename)

        self.bulletin_url = 'https://www.wbhealth.gov.in/pages/corona/bulletin'
        self.match_text = '2019 ncov bulletin as on'

    def _date_fixup_(self, date):
        
        fixup_table = {
            '27thjuly 2020': '27th july, 2020'
        }
        return fixup_table.get(date, date)


    def get_bulletin_links(self):

        html = self.get_url_html(self.bulletin_url)
        html_parsed = BeautifulSoup(html, 'html.parser')
        bulletin_anchors = [
            anchor for anchor in html_parsed.find_all('a')
            if anchor.text.lower().strip().startswith(self.match_text)
        ]

        link_dict = {}

        for anchor in bulletin_anchors:
            datestr = anchor.text.lower().split(self.match_text)[1].strip()
            datestr = self._date_fixup_(datestr)
            datestr = self.get_date_str(datestr)

            if datestr is None:
                continue

            try:
                href = anchor['href']
            except:
                pass

            link_dict[datestr] = href
        
        return link_dict

    def run(self):

        print(f'\t Downloading West Bengal bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()
        
        return bulletin_links
