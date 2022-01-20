import sqlite3
import pandas as pd
import json


def get_queries():
    CONFIGPATH = './configs/visualization.sql.json'
    with open(CONFIGPATH, 'r') as f:
        queries = json.load(f)
    return queries


def get_generic_query_result(db_uri, queryid, return_csv=True):

    queries = get_queries()
    query = queries[queryid]
    sql = query['query']
    cols = query['columns']

    data = read_from_db(db_uri, sql)
    df = pd.DataFrame(data)
    df.columns = cols

    if return_csv:
        csvdata = df.to_csv(index=False)
        return csvdata

    return df


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

def KA_gender_fatalities(db_uri):
    key = 'KA.gender.wise.fatalities'
    data = get_generic_query_result(db_uri, key, return_csv=False)
    data = data.pivot_table(index=['month'], columns=['gender'], values=['count']).fillna('N/A').reset_index()
    data = data.values.tolist()
    data = pd.DataFrame(data, columns=['month', 'fatalities (female)', 'fatalities (male)'])

    total = data['fatalities (female)'] + data['fatalities (male)']
    data['fatalities (female)'] = data['fatalities (female)'] * 100.0 / total
    data['fatalities (male)'] = data['fatalities (male)'] * 100.0 / total

    data = data.to_csv(index=False)
    return data

def KA_agewise_fatalities(db_uri):

    def transform(val):
        low = int(val/10.0) * 10
        return f'{low}-{low+10}'

    key = 'KA.age.wise.fatalities'
    data = get_generic_query_result(db_uri, key, return_csv=False)
    data['count'] = 1.0
    data['age'] = data['age'].apply(transform)
    data = data.pivot_table(index=['month'], columns=['age'], values=['count'], aggfunc='count').fillna(0).reset_index()
    data = data.T.reset_index(drop=True, level=[0]).T

    colorder = sorted(list(data.columns), key=lambda x: int(x.split('-')[0]) if x != '' else -1)
    data = data[colorder]

    cols = list(data.columns)
    cols[0] = 'Month'
    data.columns = cols 

    data = data.to_csv(index=False)
    return data

def KL_gender_fatalities(db_uri):
    key = 'KL.gender.wise.fatalities'
    data = get_generic_query_result(db_uri, key, return_csv=False)
    data = data.pivot_table(index=['month'], columns=['gender'], values=['count']).fillna('N/A').reset_index()
    data = data.values.tolist()
    data = pd.DataFrame(data, columns=['month', 'fatalities (female)', 'fatalities (male)'])

    total = data['fatalities (female)'] + data['fatalities (male)']
    data['fatalities (female)'] = data['fatalities (female)'] * 100.0 / total
    data['fatalities (male)'] = data['fatalities (male)'] * 100.0 / total

    data = data.to_csv(index=False)
    return data

def KL_agewise_fatalities(db_uri):

    def transform(val):
        low = int(val/10.0) * 10
        return f'{low}-{low+10}'

    key = 'KL.age.wise.fatalities'
    data = get_generic_query_result(db_uri, key, return_csv=False)
    data['count'] = 1.0
    data['age'] = data['age'].apply(transform)
    data = data.pivot_table(index=['month'], columns=['age'], values=['count'], aggfunc='count').fillna(0).reset_index()
    data = data.T.reset_index(drop=True, level=[0]).T

    colorder = sorted(list(data.columns), key=lambda x: int(x.split('-')[0]) if x != '' else -1)
    data = data[colorder]

    cols = list(data.columns)
    cols[0] = 'Month'
    data.columns = cols 

    data = data.to_csv(index=False)
    return data