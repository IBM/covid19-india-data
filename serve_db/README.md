# DB server

[![DB](https://img.shields.io/badge/implementation-python-green)](./serve_db.py)

This is the code serving the DB for the [landing page](https://ibm.biz/covid-data-india) to hit. To run locally:

> Install requirements.

```bash
user:~$ pip3 install -r requirements.txt
```

> Download DB and point to it from the [serve_db.py](https://github.com/IBM/covid19-india-data/blob/main/serve_db/serve_db.py#L11).

[`Download`](https://ibm.biz/covid19-india-db)

```python
__path_to_db_file = "/path/to/db"
```

> Run server. 

```bash
user:~$ python3 serve_db.py
```

