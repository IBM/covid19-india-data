from typing import List, Tuple, Union
from schemas import *

from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin

import json
import sqlite3
import os

__path_to_db_file = "covid-india.db"

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def __process_name(name: str) -> str:
    return name.replace("_", " ").capitalize()


def __process_names(names: Union[List, Tuple]) -> Tuple:
    return tuple([__process_name(item) for item in names])


@app.route("/")
def hello():
    return "COVID-19 Data from India. 8/15"


@app.route("/fetch_data", methods=['POST'])
def fetch_data(
        state_short_name: str = None, 
        filter_data: List[TableSchema] = [],
        scale_down: int = 10
    ) -> StateData:

    
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

    con = sqlite3.connect(__path_to_db_file)
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


@app.route("/fetch_schema", methods=['POST'])
def fetch_schema(state_short_name: str = None) -> StateSchema:
    
    if not state_short_name:

        payload = json.loads(request.get_data().decode('utf-8'))
        state_short_name = payload["state_short_name"]

    response = StateData(data=list())

    con = sqlite3.connect(__path_to_db_file)
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 3456)))



