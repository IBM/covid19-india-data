import sys

from datetime import datetime

from .DL import DelhiDB
from .WB import WestBengalDB
from .TG import TelanganaDB
from .HR import HaryanaDB
from .KL import KeralaDB
from .MH import MaharashtraDB

from .Metadata import MetadataDB

class DBMain(object):

    def __init__(self, datadir):
        self.datadir = datadir

        self.setup_tables()
        self.record_table_metadata()

    def setup_tables(self):
        
        self.states = {
            'DL': DelhiDB(datadir=self.datadir),
            'WB': WestBengalDB(datadir=self.datadir),
            'TG': TelanganaDB(datadir=self.datadir),
            'HR': HaryanaDB(datadir=self.datadir),
            'KL': KeralaDB(datadir=self.datadir)
            'MH': MaharashtraDB(datadir=self.datadir)
        }

        self.metatable = MetadataDB(datadir=self.datadir)

    def insert_for_state(self, state, data):

        obj = self.states[state]
        obj.insert_row(data)

    def insert_metadata(self, data):
        self.metatable.insert_row(data)

    def record_table_metadata(self):
        """ Record all the state tables information in the database """

        for state_name, db_obj in self.states.items():
            for tableobj in db_obj.tables.values():

                datum = {
                    'table_name': tableobj.table_name,
                    'state': state_name,
                    'description': tableobj.table_desc
                }

                row = {'table-overview': datum}
                self.insert_metadata(row)

    def record_bulletin_links(self, data):
        """ Record all the bulletins link in the database """

        for state_name, linkdata in data.items():
            for datestr, href in linkdata.items():
                tablerow = {
                    'date': datestr,
                    'state': state_name,
                    'bulletin_link': href
                }
                row = {'bulletin-links': tablerow}
                self.insert_metadata(row)

    def record_db_metadata(self):
        """ Record DB Metadata """

        # Store last updated
        currtime = datetime.now()
        timestr = f'{currtime.year}-{currtime.month:02d}-{currtime.day:02d}'
        tablerow = {'key': 'last-updated', 'value': timestr}
        row = {'db-properties': tablerow}
        self.insert_metadata(row)


if __name__ == '__main__':
    datadir = str(sys.argv[1])
    obj = DBMain(datadir)