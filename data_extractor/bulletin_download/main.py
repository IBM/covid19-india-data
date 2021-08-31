import sys

from bulletin_download.states.DL import Delhi
from bulletin_download.states.WB import WestBengal
from bulletin_download.states.TG import Telangana
from bulletin_download.states.TN import TamilNadu


def run(basedir):

    state_downloaders = [
        #Telangana,
        WestBengal,
        #Delhi,
        TamilNadu
    ]

    for state in state_downloaders:
        print(f'Downloading bulletins for state {state}')
        obj = state(basedir)
        obj.run()


if __name__ == '__main__':
    basedir = str(sys.argv[1])
    run(basedir)
