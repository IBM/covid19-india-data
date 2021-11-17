import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )


def identify_header_rows(table):
    
    for idx, row in table.iterrows():
        row_str = ' '.join(row).lstrip()
        if row_str.startswith('1'):
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


def process_individual_fatality_info(table):

    header_idx = identify_header_rows(table)
    datalist = [list(row) for _, row in table.iterrows()]

    # find index to left strip
    last_header_row = datalist[header_idx-1]
    for colidx in range(len(last_header_row)):
        if last_header_row[colidx].lower().startswith('sl'):
            break

    for idx in range(header_idx-1):
        datalist[idx] = forward_fill_row(datalist[idx])

    datalist = merge_header_rows(datalist, header_idx)

    # filter rows that do not start with number
    fn_filter = lambda row: row[0].replace('.','',1).isdigit()
    datalist = [datalist[0]] + [row[colidx:] for row in datalist if fn_filter(row[colidx:])]

    result = []
    for row in datalist[1:]:
        tmp = {
            'district_name': row[1].strip().lower(),
            'patient_no': row[2].strip(),
            'age': row[3],
            'sex': row[4].strip(),
            'description': row[5].strip(),
            'symptoms': ', '.join(sorted(map(lambda x: x.strip(), row[6].split(',')))),
            'comorbidities': ', '.join(sorted(map(lambda x: x.strip(), row[7].split(',')))),
            'doa': row[8],
            'dod': row[9],
        }

        if len(row) >= 10:
            tmp['place_of_death'] = row[10]

        result.append(tmp)
    
    return result
