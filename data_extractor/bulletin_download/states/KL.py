from .bulletin import Bulletin
from bs4 import BeautifulSoup

import datetime
import re


class Kerala(Bulletin):

    def __init__(self, basedir):

        statename = 'KL'
        super().__init__(basedir, statename)

        self.baseurl = 'https://dhs.kerala.gov.in'
        self.startdate = datetime.date(2020, 1, 31) # January 31 2020
        

    def get_website_html(self, date):

        day = '{:02d}'.format(date.day)
        month = '{:02d}'.format(date.month)
        year = date.year

        if date < datetime.date(2020, 3, 13):
            dummy_month = "03"
            dummy_day = "12"

        else:
            dummy_month = month
            dummy_day = day

        url = self.baseurl + f'/{year}/{dummy_month}/{dummy_day}/{day}-{month}-{year}'
        html = self.get_url_html(url)
        return html


    def parse_url(self, html):

        soup = BeautifulSoup(html, 'html.parser')

        for anchor in soup.find_all('a'):
            anchor_text = anchor.text.strip()

            if anchor_text == "English":
                return anchor.get('href')
    

    def get_bulletin_links(self):

        today = datetime.date.today()
        currdate = self.startdate
        bulletin_links = {}

        while currdate <= today:
            html = self.get_website_html(currdate)
            url = self.parse_url(html)

            if url:

                url = self.baseurl + self.parse_url(html)

                datestr = self.get_date_str(str(currdate))
                bulletin_links[datestr] = url

                print(f'\t Downloaded {datestr}')

            currdate = currdate + datetime.timedelta(days=1)
        
        return bulletin_links


    def run(self):

        print(f'\t Downloading Kerala bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links

