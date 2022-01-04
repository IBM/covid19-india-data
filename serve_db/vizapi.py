import sqlite3
import pandas as pd
import json


def hospitalization(db_uri, statename):

    with open('./configs/visualization.sql.json', 'r') as f:
        queries = json.load(f)
        hospital_query = queries['hospitalizations.queries'][statename]

    try:
        con = sqlite3.connect(db_uri, uri=True)
        cursor = con.cursor()
        cursor.execute(hospital_query)
    except Exception:
        records = ''
    else:
        records = cursor.fetchall()
    finally:
        con.close()
    

    df = pd.DataFrame.from_records(records, columns=['date', 'hospitalization'])
    csvdata = df.to_csv(index=False)
    return csvdata
