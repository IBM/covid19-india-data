from .bulletin import Bulletin
from bs4 import BeautifulSoup


class Kerala(Bulletin):

    def __init__(self, basedir):

        statename = 'KL'
        super().__init__(basedir, statename)

        self.bulletin_page_url = u'https://dhs.kerala.gov.in/%e0%b4%a1%e0%b5%86%e0%b4%af%e0%b4%bf%e0%b4%b2%e0%b4%bf-%e0%b4%ac%e0%b5%81%e0%b4%b3%e0%b5%8d%e0%b4%b3%e0%b4%b1%e0%b5%8d%e0%b4%b1%e0%b4%bf%e0%b4%a8%e0%b5%8d%e2%80%8d/'
        self.baseurl = 'https://dhs.kerala.gov.in'
        
    def get_bulletin_page_links(self):
        
        html = self.get_url_html(self.bulletin_page_url)
        soup = BeautifulSoup(html, 'html.parser')
        result = {}

        for anchor in soup.find_all('a', href=True):
            text = anchor.text.strip()
            href = anchor['href']

            try:
                if len(text.split('/')) != 3:
                    continue

                datestr = self.get_date_str(text, ['%d/%m/%Y'])
            except Exception:
                continue
            else:
                if datestr is not None:
                    result[datestr] = self.baseurl + href

        return result


    def parse_url(self, url):

        html = self.get_url_html(url)
        soup = BeautifulSoup(html, 'html.parser')

        for anchor in soup.find_all('a'):
            anchor_text = anchor.text.strip()

            if anchor_text == "English":
                return anchor.get('href')
    

    def get_bulletin_links(self):

        bulletin_page_links = self.get_bulletin_page_links()
        bulletin_links = {}

        for date, url in bulletin_page_links.items():
            bulletin_url = self.parse_url(url)
            if bulletin_url:
                bulletin_links[date] = self.baseurl + bulletin_url
        
        return bulletin_links


    def run(self):

        print(f'\t Downloading Kerala bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links
