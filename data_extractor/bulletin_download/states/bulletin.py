import os
import json
import re
import requests
import dateparser

from bs4 import BeautifulSoup
from pathlib import Path


class Bulletin(object):

    def __init__(self, basedir, statename):

        self.basedir = os.path.abspath(basedir)
        self.statename = statename
        self._statefile = os.path.join(self.basedir, 'metadata', 'bulletins', f'{self.statename}.json')
        self._bulletin_savedir = os.path.join(self.basedir, 'bulletins', self.statename)

        self._init_state_()

    def _init_state_(self):

        os.makedirs(os.path.dirname(self._statefile), exist_ok=True)
        os.makedirs(self._bulletin_savedir, exist_ok=True)

        if os.path.exists(self._statefile):
            with open(self._statefile, 'r') as f:
                self._state = json.load(f)
        else:
            self._state = {}

        if 'downloaded-bulletins' not in self._state:
            self._state['downloaded-bulletins'] = []
        if 'bulletin-paths' not in self._state:
            self._state['bulletin-paths'] = {}

    def _save_state_(self):
        with open(self._statefile, 'w') as f:
            json.dump(self._state, f)

    def download_and_save_bulletin(self, link, savedir, fname):

        fpath = os.path.join(savedir, fname)
        req = requests.get(link)

        with open(fpath, 'wb') as f:
            f.write(req.content)

    def get_url_html(self, url):

        page = requests.get(url)
        html = page.content
        return html

    def get_date_str(self, datestr):
        date = dateparser.parse(datestr)

        if date is None:
            return None
            
        datestr = f'{date.year}-{date.month:02d}-{date.day:02d}'
        return datestr

    def download_bulletins(self, bulletin_links):

        for date, link in bulletin_links.items():
            if date in self._state['downloaded-bulletins']:
                continue

            fname = f'{self.statename}-Bulletin-{date}.pdf'
            self.download_and_save_bulletin(link, self._bulletin_savedir, fname)
            self._state['downloaded-bulletins'].append(date)
            self._state['bulletin-paths'][date] = os.path.join(self._bulletin_savedir, fname)
        
        self._save_state_()
