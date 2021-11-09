import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )


def identify_header_rows(table):
    
    for idx, row in table.iterrows():
        row = list(row)
        if row[0].strip() == '1':
            break
    
    return idx


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


def convert_datadict_to_datalist(datadict):

    datalist = []
    cols = list(datadict.keys())
    n = len(datadict[cols[0]])

    for i in range(n):
        row = {col: datadict[col][i] for col in cols}
        datalist.append(row)
    
    return datalist

def convert_header_text_to_colname(datadict, keymap):

    datadict_new = {}
    processed_colnames = []

    for text, val in datadict.items():
        for colname, keys in keymap:

            if False in [key in text.lower() for key in keys] or colname in processed_colnames:
                continue
                
            datadict_new[colname] = val
        
    return datadict_new


def convert_district_table_to_dict(table):

    header_idx = identify_header_rows(table)
    datalist = [list(row) for _, row in table.iterrows()]

    for idx in range(header_idx-1):
        datalist[idx] = forward_fill_row(datalist[idx])
    
    # forward fill last row (total line)
    datalist[-1] = forward_fill_row(datalist[-1])

    datalist = merge_header_rows(datalist, header_idx)

    # Remove first column
    datalist = [x[1:] for x in datalist]

    # Convert data list to dict
    datadict = {}

    for colidx in range(len(datalist[0])):
        colname = datalist[0][colidx]
        vals = [row[colidx] for row in datalist[1:]]
        datadict[colname] = vals
    
    return datadict


def process_district_data(datadict):

    keymap = [
        ('district_name', ['name', 'district']),
        
        ('positive_cases_today', ['positive', 'case', 'today']),
        ('positive_cases_cumulative', ['positive', 'case']),
        
        ('recovered_total', ['recover', 'discharge']),
        ('recovery_rate', ['recovery', 'rate']),

        ('deaths_with_comorbidity', ['deaths', 'with ', 'comorbidity']),
        ('deaths_without_comorbidity', ['deaths', 'without', 'comorbidity']),
        ('deaths_total', ['deaths', 'no']),

        ('active_cases_less_11days', ['active', 'case', '<=', '11']),
        ('active_cases_more_11days', ['active', 'case', '>', '11']),
        ('active_cases_total', ['active', 'case']),

        ('vaccination_dose1', ['dose', '1st', 'vaccin']),
        ('vaccination_dose2', ['dose', '2nd', 'vaccin']),
        ('vaccination_total', ['cumulative', 'vaccin'])
    ]

    datadict_new = convert_header_text_to_colname(datadict, keymap)
    datadict_new = convert_datadict_to_datalist(datadict_new)
    return datadict_new


def process_critical_covid_info(table):

    header_idx = identify_header_rows(table)
    table = table.iloc[header_idx:]

    datalist = [list(row) for _, row in table.iterrows()]
    datalist[-1] = forward_fill_row(datalist[-1])

    data = []
    for row in datalist:
        tmp = {}
        tmp['facility_name'] = row[1]
        tmp['patients_on_oxygen_support'] = locale.atoi(row[2])
        tmp['patients_ventilator'] = locale.atoi(row[3])
        tmp['total_patients'] = locale.atoi(row[4])
        data.append(tmp)
    
    return data