from typing import List, Tuple, Union
from schemas import *

from flask import Flask, request, render_template, send_file
from flask_cors import CORS, cross_origin

import json
import sqlite3
import os
import dateparser

__path_to_db_file = "covid-india.db"
__db_uri = f'file:{__path_to_db_file}?mode=ro'

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def __process_name(name: str) -> str:
    return name.replace("_", " ").capitalize()


def __process_names(names: Union[List, Tuple]) -> Tuple:
    return tuple([__process_name(item) for item in names])


def __process_date(date: str) -> str:
    date = dateparser.parse(date)
    datestr = f'{date.year}-{date.month:02d}-{date.day:02d}'
    return datestr


def __scale_down_data(records: List[Tuple], scale_down: int) -> List:
    new_records = list()
    log_record = True
    day_count = 0 

    for record in records[:-1]: 

        if day_count % scale_down == 0:
            new_records.append(record)

        day_count +=1

    new_records.append(records[-1])
    return new_records


@app.route("/")
def hello():
    return "COVID-19 Data from India. 8/15"


@app.route("/download_db")
def download_db():
    return send_file(__path_to_db_file, as_attachment=True)


@app.route("/last_updated", methods=['POST'])
def last_updated():
    
    con = sqlite3.connect(__db_uri, uri=True)
    cursor = con.cursor()
    query = f"SELECT value from Metadata_DB_Properties where key='last-updated'"
    cursor.execute(query)
    records = cursor.fetchall()
    last_updated_date = records[0][0] if records else None
    
    return json.dumps({"last_updated" : last_updated_date}, indent=4)


@app.route("/fetch_data", methods=['POST'])
def fetch_data(
        state_short_name: str = None, 
        filter_data: List[TableSchema] = [],
        scale_down: int = 10
    ) -> StateData:

    
    if not state_short_name:

        payload = json.loads(request.get_data().decode('utf-8'))
        state_short_name = payload["state_short_name"]

        if not filter_data and "filter_data" in payload:
            filter_data = payload["filter_data"]

        if "scale_down" not in payload:
            scale_down = 1
        else:
            scale_down = int(payload["scale_down"])


    response = StateData(data=list())

    con = sqlite3.connect(__db_uri, uri=True)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        if table_name.startswith(state_short_name):

            new_table = DataTable()

            query = "SELECT * FROM {}".format(table_name)
            cursor.execute(query)

            records = cursor.fetchall()
            columns = next(zip(*cursor.description))

            filtered_column_data = __scale_down_data(records, scale_down)

            if not filter_data: 

                response["data"].append(
                    DataTable(
                        title = __process_name(table_name.replace("{}_".format(state_short_name), "")),
                        columns = __process_names(columns),
                        data = filtered_column_data
                    )
                )

            elif table_name in [item["title"] for item in filter_data]: 
                
                requested_columns =  list()

                for item in filter_data:
                    requested_columns += item["columns"]

                requested_columns = list(set(requested_columns) & set(columns))

                if requested_columns:

                    new_filtered_column_data = list()

                    for record in filtered_column_data: 
                        new_record = [record[0]]

                        for column in columns[1:]: 

                            if column in requested_columns:
                                new_record.append(record[columns.index(column)])

                        new_filtered_column_data.append(tuple(new_record))

                    response["data"].append(
                        DataTable(
                            title = __process_name(table_name.replace("{}_".format(state_short_name), "")),
                            columns =  __process_names(["Date" ] + requested_columns),
                            data = new_filtered_column_data
                        )
                    )


                else:

                    response["data"].append(
                        DataTable(
                            title = __process_name(table_name.replace("{}_".format(state_short_name), "")),
                            columns = __process_names(columns),
                            data = filtered_column_data
                        )
                    )

    con.close()
    return json.dumps(response, indent=4)


@app.route("/get_data", methods=['GET'])
def get_data(
        state_short_name: str = None, 
        table_name: str = None, 
        column_name: str = None, 
        sampling_rate: int = 1
    ) -> StateData:

    if not state_short_name:
        state_short_name = request.args.get('state')
        table_name = request.args.get('table')

        column_name = request.args.get('column')
        column_name = [column_name] if column_name else []

        sampling_rate = request.args.get('rate')
        sampling_rate = int(sampling_rate) if sampling_rate else 1

    response = fetch_data(state_short_name, [{"title": table_name, "columns": column_name}], sampling_rate)
    return response


@app.route("/query", methods=['POST'])
def query(query: str = None, sampling_rate: int = 1) -> TimeSeries:

    if not query:

        payload = json.loads(request.get_data().decode('utf-8'))
        query = payload["query"]

        if "scale_down" in payload:
            sampling_rate = int(payload["scale_down"])

        else:
            sampling_rate = 1

    response = TimeSeries(data=list())

    con = sqlite3.connect(__db_uri, uri=True)
    cursor = con.cursor()
    cursor.execute(query)

    temp_data = cursor.fetchall()
    response["data"] = __scale_down_data(temp_data, sampling_rate)

    con.close()
    return json.dumps(response, indent=4)


@app.route("/fetch_schema", methods=['POST'])
def fetch_schema(state_short_name: str = None) -> StateSchema:
    
    if not state_short_name:

        payload = json.loads(request.get_data().decode('utf-8'))
        state_short_name = payload["state_short_name"]

    response = StateData(data=list())

    con = sqlite3.connect(__db_uri, uri=True)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table in tables:
        table_name = table[0]

        if table_name.startswith(state_short_name):

            query = "SELECT * FROM {}".format(table_name)
            cursor.execute(query)

            new_schema = TableSchema(
                    title = table_name,
                    columns = next(zip(*cursor.description)),
                )

            response["data"].append(new_schema)

    con.close()
    return json.dumps(response, indent=4)


@app.route("/fetch_days_data", methods=['POST'])
def fetch_days_data(
        state_short_name: str = None, 
        date: str = None
    ) -> StateData:

    payload = json.loads(request.get_data().decode('utf-8'))

    if state_short_name is None:
        state_short_name = payload["state_short_name"]
    if date is None:
        date = payload["date"]
    
    date = __process_date(date)

    con = sqlite3.connect(__db_uri, uri=True)
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    table_names = [table[0] for table in tables]
    state_tables = [tablename for tablename in table_names if tablename.startswith(state_short_name)]

    # Fetch bulletin link
    query = "SELECT bulletin_link from Metadata_Bulletin_Links where date='{}' AND state='{}';".format(date, state_short_name)
    cursor.execute(query)
    records = cursor.fetchall()
    bulletin_link = records[0][0] if records else None
    
    response = DailyData(
        date=date, 
        state=state_short_name, 
        bulletin_link=bulletin_link, 
        data=[]
    )

    for table_name in state_tables:
        query = "SELECT * FROM {} WHERE date='{}';".format(table_name, date)
        cursor.execute(query)

        records = cursor.fetchall()
        columns = next(zip(*cursor.description))

        response["data"].append(
            DataTable(
                title = table_name,
                columns = columns,
                data = records
            )
        )
    
    con.close()
    
    return json.dumps(response, indent=4)


@app.route("/fetch_dashboard_data", methods=["POST"])
def fetch_dashboard_data() -> DashboardData:

    with open("./configs/dashboard.sql.json", "r") as f:
        queriesdata = json.load(f)
    
    columns = queriesdata['column.names']
    queries = queriesdata['queries']

    con = sqlite3.connect(__db_uri, uri=True)
    cursor = con.cursor()
    response = DashboardData(
        columns=columns,
        data=[]
    )

    for state_query in queries:
        state_fullname = state_query['state.full.name']
        state_shortname = state_query['state.short.name']

        # TABLE data
        querystr = ' '.join(state_query['query'])
        cursor.execute(querystr)
        table_data = list(cursor.fetchone())
        table_data.insert(0, state_fullname)

        # GRAPH data
        querystr = ' '.join(state_query['query'][:-1])
        cursor.execute(querystr)
        graph_data = __scale_down_data(list(cursor.fetchall()), 10)

        response["data"].append(
            StateDashboardData(
                state_fullname = state_fullname,
                state_shortname = state_shortname,
                table_data = table_data,
                graph_data = graph_data
            )
        )

    con.close()
    return json.dumps(response, indent=4)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3456)))

