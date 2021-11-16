import pandas as pd

from camelot.core import TableList, Table


def _merge_tables_samewidth(table1, table2):

    # return were_tables_merged = False if either of tables is None
    if table1 is None or table2 is None:
        return False, None
    
    ncols1 = table1.shape[1]
    ncols2 = table2.shape[1]

    if ncols1 != ncols2:
        return False, None

    merged_table = pd.concat([table1, table2])
    return True, merged_table


def merge_tables(table1, table2, heuristic):

    assert heuristic in ['same-table-width']

    fn_map = {
        'same-table-width': _merge_tables_samewidth
    }

    were_tabled_merged, merged_table = fn_map[heuristic](table1, table2)
    return were_tabled_merged, merged_table




def filter_tables(tables, start_page=None, end_page=None):

    # filter tables that lie between the start and the end page
    tables_filtered = []
    for table in tables:
        if start_page is not None and table.page < start_page:
            continue
        if end_page is not None and table.page > end_page:
            continue
        tables_filtered.append(table)


def group_tables_by_page(tables):
    
    tables_grouped = []
    for table in tables:
        page = table.page
        while len(tables_grouped) < page:
            tables_grouped.append([])
        tables_grouped[page].append(table.df)   # Insert only the pandas dataframe here

    return tables_grouped


def concatenate_tables(tables, heuristic, start_page=None, end_page=None):
    """
    Concatenates multi-page tables into a common tables
    """

    if not isinstance(tables, TableList):
        raise ValueError(f'`tables` attribute need to be an instance of Camelot TableList')

    # filter tables that lie between the start and the end page
    tables_filtered = filter_tables(tables, start_page, end_page)

    # group tables by page number. creates a list of list with each list being tables on a page
    tables_grouped = group_tables_by_page(tables_filtered)

    tables_concatenated = []
    for pageno in range(len(tables_grouped)):

        current_page_tables = tables_grouped[pageno]
        if len(current_page_tables) == 0:
            current_page_tables = [None]

        if pageno > 0:
            table1 = tables_concatenated[-1]
            table2 = current_page_tables[0]

            were_tables_merged, merged_table = merge_tables(table1, table2, heuristic)

            if were_tables_merged:
                tables_concatenated[-1] = merged_table
                current_page_tables.pop(0)

        tables_concatenated.extend(current_page_tables)

    # filter tables to remove None elements
    tables_concatenated = [tbl for tbl in tables_concatenated if tbl is not None]

    tablelist = TableList(tables_concatenated)
    return tablelist
