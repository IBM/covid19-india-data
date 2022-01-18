import sqlite3
import pandas as pd
import json


def get_queries():
    CONFIGPATH = './configs/visualization.sql.json'
    with open(CONFIGPATH, 'r') as f:
        queries = json.load(f)
    return queries


def get_generic_query_result(db_uri, queryid):

    queries = get_queries()
    query = queries[queryid]
    sql = query['query']
    cols = query['columns']

    data = read_from_db(db_uri, sql)
    df = pd.DataFrame(data)
    df.columns = cols
    csvdata = df.to_csv(index=False)
    return csvdata


def read_from_db(db_uri, query):
    try:
        con = sqlite3.connect(db_uri, uri=True)
        cursor = con.cursor()
        cursor.execute(query)
    except Exception as err:
        print(err)
        records = None
    else:
        records = cursor.fetchall()
    finally:
        con.close()
        return records


def hospitalization(db_uri, last_60_days=False):

    with open('./configs/visualization.sql.json', 'r') as f:
        queries = json.load(f)

    if last_60_days:
        hospital_query = queries['hospitalizations.queries.60days']
    else:
        hospital_query = queries['hospitalizations.queries']

    datadict = {}
    ALL_STATES = sorted(hospital_query.keys())
    NA = "N/A"

    for statename in ALL_STATES:
        query = hospital_query[statename]
        records = read_from_db(db_uri, query)

        if records is not None:
            for date, val in records:
                if date not in datadict:
                    datadict[date] = {key: NA for key in ALL_STATES}
                
                datadict[date][statename] = val
        
    df = pd.DataFrame.from_records(datadict).T
    df = df.reset_index()
    df.columns = ['date'] + ALL_STATES
    csvdata = df.to_csv(index=False)
    return csvdata


def hospitalization_last60days(db_uri):
    return hospitalization(db_uri, last_60_days=True)

def DL_hospitalization_overall(db_uri):
    key = 'DL.hospitalization.overall'
    return get_generic_query_result(db_uri, key)

def DL_hospitalization_60days(db_uri):
    key = 'DL.hospitalization.60days'
    return get_generic_query_result(db_uri, key)

def DL_containment_zones(db_uri):
    key = 'DL.containment.zones'
    return get_generic_query_result(db_uri, key)

def DL_rtpcr_percentage(db_uri):
    key = 'DL.rtpcr.percentage'
    return get_generic_query_result(db_uri, key)

def GA_hospitalization(db_uri):
    key = 'GA.hospitalization'
    return get_generic_query_result(db_uri, key)

def HR_gender_samples(db_uri):
    key = 'HR.gender.wise.samples'
    return get_generic_query_result(db_uri, key)

def HR_homeisolation(db_uri):
    key = 'HR.home.isolation'
    return get_generic_query_result(db_uri, key)
