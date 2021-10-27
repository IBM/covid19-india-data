import sys

from bulletin_download.states.DL import Delhi
from bulletin_download.states.WB import WestBengal
from bulletin_download.states.TG import Telangana
from bulletin_download.states.HR import Haryana


def run(basedir):

    state_downloaders = {
        'HR': Haryana,
        'TG': Telangana,
        'WB': WestBengal,
        'DL': Delhi
    }
    
    bulletin_links = {}

    for state_name, state_obj in state_downloaders.items():
        print(f'Downloading bulletins for state {state_name}')
        obj = state_obj(basedir)
        state_bulletin_links = obj.run()
        bulletin_links[state_name] = state_bulletin_links

    return bulletin_links


if __name__ == '__main__':
    basedir = str(sys.argv[1])
    run(basedir)