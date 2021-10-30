import sqlite3
from .db import DB


class PsychosocialSupport(DB):

    def __init__(self):
        super().__init__()

        self.table_name = 'KL_psychosocial_support'
        self.table_desc = 'Psychosocial support provided through the program Ottakalla Oppamundu'
        self.cols = self.getcolumns()

    def getcolumns(self):
        cols = {
            'date': 'DATE NOT NULL',
            'psychosocial_workers': 'INT',
            'calls_to_persons_in_surveillance': 'INT',
            'followup_calls': 'INT',
            'post_covid_calls': 'INT',
            'calls_special': 'INT',
            'calls_to_school_children': 'INT',
            'calls_to_health_care_workers': 'INT',
            'calls_received_helpline': 'INT',
            'calls_total': 'INT'
        }
        return cols
