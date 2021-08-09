import re

from .bulletin import Bulletin
from bs4 import BeautifulSoup


class Delhi(Bulletin):

    def __init__(self, basedir):

        statename = 'DL'
        super().__init__(basedir, statename)

        self.baseurl = 'http://health.delhigovt.nic.in'
        self.bulletin_url = self.baseurl + '/wps/wcm/connect/doit_health/Health/Home/Covid19/Bulletin+{}+{}'
        self._bulletin_link_regex = re.compile(r'^bulletin.*dated (.*)', re.IGNORECASE)
        
        self._months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 
                        'September', 'October', 'November', 'December']
        self._years = ['2020', '2021']

    def get_website_html(self, month, year):
        url = self.bulletin_url.format(month, year)
        html = self.get_url_html(url)
        return html

    def get_bulletin_links(self, html):

        soup = BeautifulSoup(html, 'html.parser')
        link_dict = {}

        for anchor in soup.find_all('a'):
            anchor_text = ' '.join(anchor.text.lower().split())
            match = self._bulletin_link_regex.match(anchor_text)

            if not match:
                continue

            date = match.group(1)
            datestr = self.get_date_str(date)

            try:
                href = anchor['href']
            except:
                pass

            link_dict[datestr] = self.baseurl + href
        
        return link_dict
    
    def run(self):

        for year in self._years:
            for month in self._months:

                if year == '2020' and month in ['March', 'April', 'May']:
                    continue

                if year == '2020' and month == 'April':
                    month = 'Apr'
                
                print(f'\t Downloading Delhi bulletins for year {year} and month {month}')

                html = self.get_website_html(month, year)
                bulletin_links = self.get_bulletin_links(html)
                self.download_bulletins(bulletin_links)

        self._save_state_()


if __name__ == '__main__':
    obj = Delhi('/Users/mayank.agarwal@ibm.com/Documents/projects/covid-19/covid-india-data/localstore')
    obj.run()