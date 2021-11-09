from .bulletin import Bulletin

import datetime


class Maharashtra(Bulletin):

    def __init__(self, basedir):

        statename = 'MH'
        super().__init__(basedir, statename)

        self.bulletin_url = 'https://arogya.maharashtra.gov.in/pdf/ncovidepressnote{}{:02d}.pdf'
        self.startdate = datetime.date(2020, 11, 1)      # November 1, 2021

    def get_bulletin_links(self):

        today = datetime.date.today()
        currdate = self.startdate
        link_dict = {}

        while currdate <= today:
            day = currdate.day
            month = currdate.month
            year = currdate.year
            month_str = currdate.strftime('%B').lower()

            url = self.bulletin_url.format(month_str, day)

            datestr = self.get_date_str(str(currdate))
            link_dict[datestr] = url

            currdate = currdate + datetime.timedelta(days=1)
        
        return link_dict

    def run(self):

        print(f'\t Downloading Maharashtra bulletins')
        bulletin_links = self.get_bulletin_links()
        self.download_bulletins(bulletin_links)
        self._save_state_()

        return bulletin_links
