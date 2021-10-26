from typing import List, Tuple, TypedDict

class TimeSeries(TypedDict):
    data: List[Tuple] 


class TableSchema(TypedDict):
    title: str = None
    columns: Tuple[str]
       

class DataTable(TypedDict):
    title: str = None
    columns: Tuple[str]
    data: TimeSeries
       

class StateSchema(TypedDict):
    data: List[TableSchema]


class StateData(TypedDict):
    data: List[DataTable]


class DailyData(TypedDict):
    date: str
    state: str
    bulletin_link: str
    data: List[DataTable]


class StateDashboardData(TypedDict):
    state_fullname: str
    state_shortname: str
    data: List[str]

class DashboardData(TypedDict):
    columns: List[str]
    data: List[StateDashboardData]