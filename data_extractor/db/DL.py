import sqlite3

from .db import Database
from .DL_tables import DL_patient_mgmt, DL_testing_status, DL_vaccination, \
    DL_case_info, DL_containment, DL_cumulative, DL_hospitalizations

class DelhiDB(Database):

    def __init__(self, datadir):
        super().__init__(datadir)

        self.init_tables()
        self.create_tables()

    def init_tables(self):
        """
        Initializes all the tables for the particular state
        """

        self.tables = {
            'patient-management': DL_patient_mgmt.PatientMgmtTable(),
            'testing': DL_testing_status.TestingStatusTable(),
            'vaccination': DL_vaccination.VaccinationTable(),
            'case-info': DL_case_info.CaseInfoTable(),
            'containment': DL_containment.ContainmentTable(),
            'cumulative': DL_cumulative.CumulativeTable(),
            'hospitalizations': DL_hospitalizations.HospitalizationsTable()
        }

    def insert_row(self, data):
        
        cursor = self.conn.cursor()

        test_data = data.get('testing_vals', None)
        if test_data is not None:
            self.tables['testing'].insert_row(cursor=cursor, **test_data)

        vax_data = data.get('vaccination_vals', None)
        if vax_data is not None:
            self.tables['vaccination'].insert_row(cursor=cursor, **vax_data)

        hospital_data = data.get('hospital_vals', None)
        if hospital_data is not None:
            self.tables['patient-management'].insert_row(cursor=cursor, **hospital_data)

        containment_data = data.get('containment_vals', None)
        if containment_data is not None:
            self.tables['containment'].insert_row(cursor=cursor, **containment_data)

        case_info_today = data.get('case_info_vals', None)
        if case_info_today is not None:
            self.tables['case-info'].insert_row(cursor=cursor, **case_info_today)

        cumulative_case_info = data.get('cumulative_case_info', None)
        if cumulative_case_info is not None:
            self.tables['cumulative'].insert_row(cursor=cursor, **cumulative_case_info)

        hospitalization_info = data.get('hospitalizations_info', None)
        if hospitalization_info is not None:
            self.tables['hospitalizations'].insert_row(cursor=cursor, **hospitalization_info)

        self.conn.commit()
        