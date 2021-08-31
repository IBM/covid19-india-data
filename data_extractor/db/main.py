import sys

from .DL import DelhiDB
from .WB import WestBengalDB
from .TG import TelanganaDB
from .TN import TamilNaduDB


class DBMain(object):

    def __init__(self, datadir):
        self.datadir = datadir
        self.setup_tables()

    def setup_tables(self):
        
        self.states = {
            'DL': DelhiDB(datadir=self.datadir),
            'WB': WestBengalDB(datadir=self.datadir),
            'TG': TelanganaDB(datadir=self.datadir),
            'TN': TamilNaduDB(datadir=self.datadir)
        }

    def insert_for_state(self, state, data):

        obj = self.states[state]
        obj.insert_row(data)


if __name__ == '__main__':
    datadir = str(sys.argv[1])
    obj = DBMain(datadir)
