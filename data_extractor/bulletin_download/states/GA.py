from .bulletin import Bulletin
from bs4 import BeautifulSoup

class Goa(Bulletin):

    def __init__(self, basedir):

        statename = 'GA'
        super().__init__(basedir, statename)


    def get_urls(self, url: str):
        
        try:
            html = self.get_url_html(url)
        except:
            print(f'ERROR: Downloading Goa bulletins from url {url} failed')
            return dict()
             
        soup = BeautifulSoup(html, 'html.parser')

        baseurl = 'https://www.goa.gov.in/wp-content/uploads'
        bulletin_links = dict()

        for anchor in soup.find_all('a'):

            anchor_href = anchor.get('href')

            if anchor_href:

                if "media-bulletin-" in anchor_href.lower() and anchor_href.startswith(baseurl):

                    try: 
                        date_time_str = anchor_href.lower().split("media-bulletin-")[1].split(".pdf")[0]
                        stop_words = ["-pdf", "dated-", "-1", "" "-revised", "-main", "-converted"]

                        for sw in stop_words:
                            date_time_str = date_time_str.replace(sw, "")

                        for i in range(10):
                            if date_time_str.endswith(f"-{i}"):
                                "-".join(date_time_str.split("-")[:-1])

                        date_time_str = date_time_str.replace("-", " ")
                        date_time_str = date_time_str.replace("_", "-")

                        datestr = self.get_date_str(date_time_str)

                        bulletin_links[datestr] = anchor_href

                    except: pass

        return bulletin_links



    def get_bulletin_links(self):

        archive_url = "https://www.goa.gov.in/covid-19-archives/"
        current_url = "https://www.goa.gov.in/covid-19/"

        current_urls = self.get_urls(current_url)
        archived_urls = self.get_urls(archive_url)

        return {**archived_urls, **current_urls}


    def run(self):

        print(f'\t Downloading Goa bulletins')

        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links
