import numpy as np
import dateparser
import camelot
import tabula
import pandas as pd
import math

from pdfminer.high_level import extract_pages


def clean_numbers_str(text):
    chars = ['%', '*']

    if type(text) != str or text is None:
        return text

    for ch in chars:
        text = text.replace(ch, '')
    
    return text.strip()


def are_keywords_in_table(df, keywords):

    found = []
    table = [df.columns.values.tolist()] + df.values.tolist()
    table = [x.lower().strip() for x in np.array(table).flatten()]

    for word in keywords:
        for text in table:
            if word in text:
                found.append(word)
                break
    
    return len(keywords) == len(found)

def find_table_by_keywords(tables, keywords):

    for table in tables:
        if isinstance(table, pd.DataFrame):
            table_df = table
        else:
            table_df = table.df

        if are_keywords_in_table(table_df, keywords):
            return table_df
    return None


def find_all_tables_by_keywords(tables, keywords):
    result = []
    for table in tables:
        table_df = table.df
        if are_keywords_in_table(table_df, keywords):
            result.append(table_df)
    return result


def convert_df_to_dict(df, key_idx, val_idx, remove_nan=True):
    keys = df.values[:, key_idx]
    vals = df.values[:, val_idx]

    if remove_nan:
        df_dict = dict()

        for k, v in zip(keys, vals):
            if type(k) == float and k != k:
                continue
            df_dict[k] = v
    else:
        df_dict = {k:v for (k, v) in zip(keys, vals)}

    return df_dict

def add_values_from_neighbors(df, df_dict, key_idx, val_idx):
    # idea is to check till when is the value empty and all hose indices
    # in value should go to the current index
    # for example consider key list ["", "total number #", ""]
    # and value list ["", "", "12345"]
    # it is happening in case of Tamil Nadu table on Page number 2
    # consider this to be a sort of a patch
    keys = df.values[:, key_idx]
    vals = df.values[:, val_idx]
    keys_list = keys.tolist()
    length = len(keys)

    for k, v in df_dict.items():
        # check if the dict doesnt have any value
        if k in df_dict and df_dict[k] == "":
            value = ""
            index = keys_list.index(k)
            # check previous neighbors
            counter = 1
            check_previous_neighbor = True
            if index - 1 > 0 and keys[index - 1] == "":
                # prepend the value
                value = vals[index - counter] + value

            # check next neighbors
            if index + 1 < length and keys[index + counter] == "":
               # append the value
               value += vals[index + counter]

            df_dict[k] = value

    return df_dict

def extract_info_from_table_by_keywords(df_dict, keymap):

    result = {}
    for text, val in df_dict.items():
        for id, keys in keymap.items():
            if False in [key in text.lower() for key in keys]:
                continue
            result[id] = val

    return result

def parse_dates(datestr):

    date = dateparser.parse(datestr)
    datestr = f'{date.year}-{date.month}-{date.day}'
    return datestr


def n_pages_in_pdf(pdf_fpath):
    pages = list(extract_pages(pdf_fpath))
    return len(pages)


def get_tables_from_pdf_camelot(pdf_fpath, pages=None, use_stream=False):

    pagerange = "1-end" if pages is None else ','.join(map(str, pages))
    _flavor = "stream" if use_stream else "lattice"
    tables = camelot.read_pdf(pdf_fpath, pages=pagerange, flavor=_flavor, strip_text='\n', split_text=True)
    return tables


def get_tables_from_pdf_tabula(pdf_fpath, pages=None):
    pagerange = "all" if pages is None else pages
    tables = tabula.read_pdf(pdf_fpath, pages=pagerange)
    return tables


def get_tables_from_pdf(library, pdf_fpath, pages=None, use_stream=False):

    if library.lower().strip() == 'camelot':
        return get_tables_from_pdf_camelot(pdf_fpath, pages, use_stream)
    elif library.lower().strip() == 'tabula':
        return get_tables_from_pdf_tabula(pdf_fpath, pages)
