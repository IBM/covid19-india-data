from .bulletin import Bulletin

import datetime


class Haryana(Bulletin):

    def __init__(self, basedir):

        statename = 'HR'
        super().__init__(basedir, statename)

        # this URL works only for dates >= 01/01/2021
        self.bulletin_url = 'http://www.nhmharyana.gov.in/WriteReadData/userfiles/file/CoronaVirus/Daily Bulletin of COVID 19 as on {:02d}-{:02d}-{}.pdf'
        self.startdate = datetime.date(2021, 1, 1)      # Jan 1, 2021

    def get_bulletin_links(self):

        today = datetime.date.today()
        currdate = self.startdate
        link_dict = {}

        while currdate <= today:
            day = currdate.day
            month = currdate.month
            year = currdate.year

            url = self.bulletin_url.format(day, month, year)
            datestr = self.get_date_str(str(currdate))
            link_dict[datestr] = url

            currdate = currdate + datetime.timedelta(days=1)
        
        return link_dict

    def run(self):

        print(f'\t Downloading Haryana bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links
