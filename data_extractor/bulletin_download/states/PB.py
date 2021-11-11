from .bulletin import Bulletin
from bs4 import BeautifulSoup
import json


class Punjab(Bulletin):
    def __init__(self, basedir):

        statename = 'PB'
        super().__init__(basedir, statename)

        self.base_html = 'http://covaprod.punjab.gov.in/covid-response.html?language=e'
        self.root_url = 'http://covaprod.punjab.gov.in/'
        self.report_js_search_string = 'report.js'


    def get_bulletin_links(self):

        html = self.get_url_html(self.base_html)
        html_parsed = BeautifulSoup(html, 'html.parser')

        for tag in html_parsed.find_all('script'):
            if "report.js" in tag.get("src"):
                report_tag = tag
                break

        report_url = self.root_url + report_tag.get("src")
        report = self.get_url_html(report_url)
        report_parsed = BeautifulSoup(report, 'lxml').contents[0]

        # hack for getting the urls from the javascript code returned
        report_parsed = str(report_parsed.get_text)

        # there is a variable `mediaarr` in the js file which has all the urls
        url_content = report_parsed.split("var mediaarr = ")[1]
        url_content = url_content[1:url_content.index("];")]

        # formatting the string content to parse as a json object
        url_content = url_content.replace("`", "'")
        url_content = url_content.replace('"',"'")
        url_content = url_content.replace("html", '"html"')
        url_content = url_content.replace("date", '"date"')
        url_content = url_content.replace("'<a", '"<a')
        url_content = url_content.replace(">'", '>"')
        url_content = url_content.replace(": '", ': "')
        url_content = url_content.replace("'", "\'")

        urls = url_content.split("},")
        links = dict()
        for s in urls:
            # special cases in the urls
            if s.count("href") > 1:
                # this means it has more than one bulletin urls
                s_arr = s.split("}")
                for h in s_arr:
                    if "href" not in h:
                        continue

                    h = h.strip()
                    if h[0] == ",":
                        h = h[1:]

                    datestr, link = self.get_date_url(h)
                    links[datestr] = link

                continue

            elif "&amp;" in s:
                # find last index of &amp; and check if its after date
                # need to remove this &amp; from the date
                # this means that the bulletin is for more than 1 dates
                index_amp = s.rfind("&amp;")
                index_date = s.rfind("date")
                if index_amp > index_date:
                    s = s[0: index_amp -1] + "'"

            elif s.count("href") == 0:
                # this means there are no bulletins
                continue
            datestr, link = self.get_date_url(s)
            links[datestr] = link

        return links

    def get_date_url(self, html_str):
        html_str = html_str.strip()[0:-1] + "\"}"
        obj = json.loads(html_str)
        anchor = BeautifulSoup(obj["html"], "html.parser").find_all("a")[0]
        link = self.root_url + anchor.get("href")
        datestr = self.get_date_str(obj["date"]) # original dd-mm-yyyy format

        return datestr, link

        

    def run(self):

        print(f'\t Downloading Punjab bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()
        
        return bulletin_links

if __name__ == "__main__":
    pb = Punjab("../Downloads")
    pb.run()
