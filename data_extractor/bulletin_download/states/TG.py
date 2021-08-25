from .bulletin import Bulletin

import datetime


class Telangana(Bulletin):

    def __init__(self, basedir):

        statename = 'TG'
        super().__init__(basedir, statename)

        self.bulletin_url = 'https://covid19.telangana.gov.in/wp-content/uploads/{}/{:02d}/Media-Bulletin-{:02d}-{:02d}-{}.pdf'
        self.startdate = datetime.date(2020, 5, 1)      # May 1 2020

    def get_bulletin_links(self):

        today = datetime.date.today()
        currdate = self.startdate
        link_dict = {}

        while currdate <= today:
            day = currdate.day
            month = currdate.month
            year = currdate.year

            url = self.bulletin_url.format(year, month, day, month, year)
            datestr = self.get_date_str(str(currdate))
            link_dict[datestr] = url

            currdate = currdate + datetime.timedelta(days=1)
        
        return link_dict

    def run(self):

        print(f'\t Downloading Telangana bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links
