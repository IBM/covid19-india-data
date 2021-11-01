from .bulletin import Bulletin
from bs4 import BeautifulSoup


class Uttarakhand(Bulletin):

    def __init__(self, basedir):

        statename = 'UK'
        super().__init__(basedir, statename)

        self.bulletin_urls = [
            "https://health.uk.gov.in/pages/view/151-covid19-health-bulletin-for-uttarakhand-page-10",
            "https://health.uk.gov.in/pages/view/148-covid19-health-bulletin-for-uttarakhand-page-9",
            "https://health.uk.gov.in/pages/view/142-covid19-health-bulletin-for-uttarakhand-page-8",
            "https://health.uk.gov.in/pages/view/135-covid19-health-bulletin-for-uttarakhand-page-7",
            "https://health.uk.gov.in/pages/view/133-covid19-health-bulletin-for-uttarakhand-page-from-december-2020-onwards",
            "https://health.uk.gov.in/pages/view/101-covid19-health-bulletin-for-uttarakhand-6",
            "https://health.uk.gov.in/pages/view/110-covid19-health-bulletin-for-uttarakhand-page-5",
            "https://health.uk.gov.in/pages/view/111-covid19-health-bulletin-for-uttarakhand-page-4",
            "https://health.uk.gov.in/pages/view/129-covid19-health-bulletin-for-uttarakhand-page-3",
            "https://health.uk.gov.in/pages/view/131-covid19-health-bulletin-for-uttarakhand-page-2",
            "https://health.uk.gov.in/pages/view/134-covid19-health-bulletin-for-uttarakhand-page-01",
        ]
        self.match_text = "Health Bulletin COVID 19_Uttarakhand_"

    def _date_fixup_(self, date):

        fixup_table = {
            '27thjuly 2020': '27th july, 2020'
        }
        return fixup_table.get(date, date)

    def get_bulletin_links(self):

        link_dict = {}

        for url in self.bulletin_urls:
            html = self.get_url_html(url)
            html_parsed = BeautifulSoup(html, 'html.parser')
            bulletin_anchors = [
                anchor for anchor in html_parsed.find_all('a')
                if anchor.text.strip().startswith(self.match_text)
            ]
            for anchor in bulletin_anchors:
                datestr = anchor.text.split(self.match_text)[1].strip()
                datestr = self._date_fixup_(datestr)
                datestr = self.get_date_str(datestr)

                if datestr is None:
                    continue

                try:
                    href = anchor['href']
                    link_dict[datestr] = "https://health.uk.gov.in" + href
                except:
                    pass

        return link_dict

    def run(self):

        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links


if __name__ == '__main__':
    obj = Uttarakhand('.')
    obj.run()
