from .db import Database
from .Metadata_tables import TableOverview, BulletinLinks, DBProperties

class MetadataDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'table-overview': TableOverview.TableOverview(),
            'bulletin-links': BulletinLinks.BulletinLinks(),
            'db-properties': DBProperties.DBProperties()
        }
        