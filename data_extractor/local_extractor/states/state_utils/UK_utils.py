import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re
import pandas as pd
import numpy as np


def clean_numbers_str(text):
    chars = ['%', '*', '#']

    if type(text) != str or text is None:
        return text

    for ch in chars:
        text = text.replace(ch, '')
    
    return text.strip()


def str2int(numstr, replace_chars=True):

    if replace_chars:
        numstr = clean_numbers_str(numstr)
    num = locale.atoi(numstr)
    return num


def str2float(numstr, replace_chars=True):

    if replace_chars:
        numstr = clean_numbers_str(numstr)
    num = locale.atof(numstr)
    return num


def is_row_header(row):
    """
    Check if the provided row is a header row or not
    It does so by checking if there are any numbers in the row text or not
    """

    for col in row:
        if re.match(r'[0-9]+', col):
            return False
    return True


def identify_header_rows(table):

    for idx, row in table.iterrows():
        row = list(row)
        if not is_row_header(row):
            break
    return idx


def is_row_empty(row):

    for col in row:
        if col.strip() != '':
            return False
    return True


def forward_fill_row(row):

    last_val = row[0]
    for i in range(1, len(row)):
        if row[i].strip() == '':
            row[i] = last_val
        else:
            last_val = row[i]
    
    return row


def merge_header_rows(datalist, header_idx):

    header_rows = datalist[:header_idx]
    data_rows = datalist[header_idx:]
    header = [' '.join(x).strip() for x in zip(*header_rows)]
    datalist_merged = [header] + data_rows
    return datalist_merged


def convert_header_text_to_colname(datadict, keymap):

    datadict_new = {}
    processed_colnames = []

    for text, val in datadict.items():
        for colname, keys in keymap:

            if False in [key in text.lower() for key in keys] or colname in processed_colnames:
                continue
                
            datadict_new[colname] = val
            processed_colnames.append(colname)
        
    return datadict_new


def convert_datadict_to_datalist(datadict):

    datalist = []
    cols = list(datadict.keys())
    n = len(datadict[cols[0]])

    for i in range(n):
        row = {col: datadict[col][i] for col in cols}
        datalist.append(row)
    
    return datalist


def _combine_negative_today_cols(df):
    cols = [x.lower().strip() for x in df.columns]
    idx1, idx2 = None, None

    for idx, colname in enumerate(cols):
        if colname.startswith('negative') and colname.endswith('govt. lab'):
            idx1 = idx
        if colname.startswith('negative') and colname.endswith('pvt. lab'):
            idx2 = idx
    if idx1 is None and idx2 is None:
        return df
    
    col1 = df.columns[idx1]
    col2 = df.columns[idx2]
    df['Negative in last 24 hours'] = df[col1] + df[col2]
    df = df.drop([col1, col2], axis=1)
    return df


def _drop_positive_govt_pvt_cols(df):
    cols = [x.lower().strip() for x in df.columns]
    idx1, idx2, idx3 = None, None, None

    for idx, colname in enumerate(cols):
        
        if False not in [key in colname.lower() for key in ['positive', 'today', 'govt', 'lab']]:
            idx1 = idx
        
        if False not in [key in colname.lower() for key in ['positive', 'today', 'pvt', 'lab']]:
            idx2 = idx

        if False not in [key in colname.lower() for key in ['positive', 'total', 'today']]:
            idx3 = idx

    if idx1 is None and idx2 is None:
        return df

    col1 = df.columns[idx1]
    col2 = df.columns[idx2]

    if idx3 is None:
        # earlier bulletins don't have total positive column. add it manually
        df['positive in last 24 hours'] = df[col1] + df[col2]
    else:
        col3 = df.columns[idx3]
        df = df.rename(columns={col3: 'positive in last 24 hours'})

    df = df.drop([col1, col2], axis=1)
    return df


def process_district_testing_table(table):

    header_idx = identify_header_rows(table)
    datalist = [list(row) for _, row in table.iterrows()]

    for idx in range(header_idx - 1):
        datalist[idx] = forward_fill_row(datalist[idx])

    for idx in range(header_idx, len(datalist)):
        row = datalist[idx]
        datalist[idx] = [str2int(val) if colidx !=0 else val for colidx, val in enumerate(row)]

    datalist = merge_header_rows(datalist, header_idx)
    df = pd.DataFrame(datalist[1:], columns=datalist[0])
    
    df = _combine_negative_today_cols(df)
    df = _drop_positive_govt_pvt_cols(df)

    datalist = [list(row) for _, row in df.iterrows()]
    cols = df.columns

    # Convert data list to dict
    datadict = {}

    for colidx in range(len(datalist[0])):
        colname = cols[colidx]
        vals = [row[colidx] for row in datalist]
        datadict[colname] = vals

    keymap = [
        ('district_name', ['district']),
        ('samples_results_awaited', ['result', 'awaited']),
        ('samples_collected_today', ['sample', 'sent', 'today']),
        ('samples_collected_cumulative', ['sample', 'cumulative']),
        ('negative_results_today', ['negative', '24', 'hour']),
        ('negative_results_total', ['negative', 'cumulative']),
        ('positive_results_total', ['positive', 'cumulative']),
        ('positive_results_today', ['positive', '24', 'hour']),
        ('rejected_samples', ['reject', 'repeat', 'sample'])
    ]

    datadict = convert_header_text_to_colname(datadict, keymap)
    datadict = convert_datadict_to_datalist(datadict)

    return datadict


def process_mucormycosis_table(table, old_format):

    header_idx = identify_header_rows(table)
    datalist = [list(row) for _, row in table.iterrows()]

    for idx in range(header_idx - 1):
        datalist[idx] = forward_fill_row(datalist[idx])
    
    datalist = merge_header_rows(datalist, header_idx)
    
    df = pd.DataFrame(datalist[1:], columns=datalist[0])
    df[df == ''] = np.NaN
    df.fillna(method='ffill', axis=0, inplace=True)

    datalist = []

    if old_format:
        n = df.shape[0]

        for idx, row in df.iterrows():

            if idx == n-1:
                tmp = {
                    'district_name': row[0].strip(),
                    'hospital_name': None,
                    'cases_total': str2int(row[3]),
                    'deaths_total': str2int(row[4]),
                    'discharged_total': str2int(row[5])
                }
            else:
                tmp = {
                    'district_name': row[1].strip(),
                    'hospital_name': row[2].strip(),
                    'cases_total': str2int(row[3]),
                    'deaths_total': str2int(row[4]),
                    'discharged_total': str2int(row[5])
                }

            datalist.append(tmp)

    else:
        for _, row in df.iterrows():
            tmp = {
                'district_name': row[0].strip(),
                'hospital_name': row[1].strip(),
                'cases_new': str2int(row[2]),
                'deaths_new': str2int(row[3]),
                'discharged_new': str2int(row[4]),
                'cases_total': str2int(row[5]),
                'deaths_total': str2int(row[6]),
                'discharged_total': str2int(row[7]),
                'migrated_total': str2int(row[8])
            }
            
            if tmp['district_name'] == 'Total':
                tmp['hospital_name'] = None

            datalist.append(tmp)

    return datalist