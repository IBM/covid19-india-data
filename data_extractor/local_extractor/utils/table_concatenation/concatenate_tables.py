from camelot.core import TableList, Table


def _merge_tables_samewidth(table1, table2):
    pass


def merge_tables(table1, table2, heuristic):

    assert heuristic in ['same-table-width']




def filter_tables(tables, start_page=None, end_page=None):

    # filter tables that lie between the start and the end page
    tables_filtered = []
    for table in tables:
        if start_page is not None and table.page < start_page:
            continue
        if end_page is not None and table.page > end_page:
            continue
        tables_filtered.append(table)


def concatenate_tables(tables, heuristic, start_page=None, end_page=None):
    """
    Concatenates multi-page tables into a common tables
    """

    if not isinstance(tables, TableList):
        raise ValueError(f'`tables` attribute need to be an instance of Camelot TableList')

    # filter tables that lie between the start and the end page
    tables_filtered = filter_tables(tables, start_page, end_page)

    # group tables by page number. creates a list of list with each list being tables on a page
    tables_pages = []
    for table in tables_filtered:
        page = table.page
        while len(tables_pages) < page:
            tables_pages.append([])
        tables_pages[page].append(table)


    tables_concatenated = []

    for idx, pagetables in enumerate(tables_pages):

        # last page tables. then just add all tables and break
        if idx == len(tables_pages) - 1:
            tables_concatenated.extend(pagetables)
            break
        
        # add current page tables to tables_concatenated
        tables_concatenated.extend(pagetables)
        were_tables_merged, merged_table = merge_tables(tables_concatenated[-1], tables_pages[idx+1], heuristic)

        # tables were merged. two things need to happen
        #   1) last table in `tables_concatenated` need to be delete
        #   2) first table from next page tables need to be deleted
        #   3) merged table needs to be added to tables_concatenated
        
        if were_tables_merged:
            tables_concatenated.pop()
            tables_pages[idx+1].pop(0)
            tables_concatenated.append(merged_table)

    tablelist = TableList(tables_concatenated)
    return tablelist
