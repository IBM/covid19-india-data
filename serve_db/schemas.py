from typing import List, Tuple, TypedDict

class TableSchema(TypedDict):
    title: str = None
    columns: Tuple[str]
       

class DataTable(TypedDict):
    title: str = None
    columns: Tuple[str]
    data: List[Tuple] 
       

class StateSchema(TypedDict):
    data: List[TableSchema]


class StateData(TypedDict):
    data: List[DataTable]

