import sys

from bulletin_download.states.DL import Delhi
from bulletin_download.states.HR import Haryana
from bulletin_download.states.KA import Karnataka
from bulletin_download.states.KL import Kerala
from bulletin_download.states.MH import Maharashtra
from bulletin_download.states.PB import Punjab
from bulletin_download.states.TG import Telangana
from bulletin_download.states.UK import Uttarakhand
from bulletin_download.states.WB import WestBengal
from bulletin_download.states.TN import TamilNadu


def run(basedir, state_to_execute=None):

    state_downloaders = {
        'DL': Delhi,
        'HR': Haryana,
        'KA': Karnataka,
        'KL': Kerala,
        'MH': Maharashtra,
        'TG': Telangana,
        'UK': Uttarakhand,
        'WB': WestBengal,
        'TN': TamilNadu
    }

    bulletin_links = {}

    for state_name, state_obj in state_downloaders.items():

        if state_to_execute is not None and state_name not in state_to_execute:
            continue

        print(f'Downloading bulletins for state {state_name}')
        obj = state_obj(basedir)
        state_bulletin_links = obj.run()
        bulletin_links[state_name] = state_bulletin_links

    return bulletin_links


if __name__ == '__main__':
    basedir = str(sys.argv[1])
    run(basedir)
