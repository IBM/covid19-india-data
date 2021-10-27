import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

import re


def is_row_header(row):
    """
    Check if the provided row is a header row or not
    It does so by checking if there are any numbers in the row text or not
    """

    for col in row:
        if re.match(r'[0-9]+', col):
            return False
    return True


def is_row_empty(row):

    for col in row:
        if col.strip() != '':
            return False
    return True


def process_caseinfo_table(df):

    datadict = {}

    dflist = [list(row) for _, row in df.iterrows() if not is_row_header(row) and not is_row_empty(row)]

    # filter list data
    dflist_filtered = [
        y.strip() for x in dflist 
        for y in x 
        if (y.strip() != '' and re.match('^\d\.{0,1}$', y.strip()) is None)
    ]

    dflist_filtered = [x for x in dflist_filtered if x.lower().strip() != 'telangana india']

    for i in range(0, len(dflist_filtered), 2):
        datadict[dflist_filtered[i]] = dflist_filtered[i+1]

    return datadict


def process_testing_table(df):

    datadict = {}
    dflist = [list(row) for _, row in df.iterrows() if not is_row_header(row) and not is_row_empty(row)]

    # filter list data
    dflist_filtered = [
        y.strip() for x in dflist
        for y in x
        if (y.strip() != '' and re.match('^\d\.{0,1}$', y.strip()) is None)
    ]

    for i in range(0, len(dflist_filtered), 2):
        datadict[dflist_filtered[i]] = dflist_filtered[i+1]

    return datadict


def process_agewise_table(df):

    datadict = {}

    col_order = [
            'ages_upto_10', 'ages_11_to_20', 'ages_21_to_30', 'ages_31_to_40', 'ages_41_to_50',
            'ages_51_to_60', 'ages_61_to_70', 'ages_71_to_80', 'ages_81_and_above', 'total'
        ]
    subcol_order = ['total', 'male', 'female']

    dflist = [
        list(row) for _, row in df.iterrows() 
        if not is_row_header(row) and not is_row_empty(row)
    ]

    colidx = 0
    for row in dflist:
        datadict[col_order[colidx] + '_' + subcol_order[0]] = locale.atof(row[-3].strip())
        datadict[col_order[colidx] + '_' + subcol_order[1]] = locale.atof(row[-2].strip())
        datadict[col_order[colidx] + '_' + subcol_order[2]] = locale.atof(row[-1].strip())

        colidx += 1

    return datadict


def process_district_case_table(df):

    result = []

    dflist = [
        list(row) for _, row in df.iterrows() 
        if not is_row_header(row) and not is_row_empty(row)
    ]

    for row in dflist:

        tmp = {
            'district': row[-2].lower(),
            'cases_new': locale.atoi(row[-1])
        }
        result.append(tmp)
    
    return result
