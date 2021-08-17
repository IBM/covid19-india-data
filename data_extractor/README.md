# Data extraction pipeline

The data extraction pipeline is responsible for (a) downloading the health bulletins from the respective sources, (b) Setting up the database tables for all the states, and (c) Extracting the information from the health bulletins and inserting these records in the database


## Directory Structure

The data extraction pipeline is structured as follows:

1. [`run.py`](./data_extractor/run.py) - Main script used to either create the database from scratch or update an existing database
2. [`bulletin_download`](./data_extractor/bulletin_download) - Downloades the health bulletins from the respective state sources, and saves them locally
   - [`main.py`](./data_extractor/bulletin_download/main.py) - Main file that orchestrates the bulletin download routine for all states
   - [`states`](./data_extractor/bulletin_download/states) -  This folder contains bulletin download scripts for each individual states. See the scripts for [Delhi](./data_extractor/bulletin_download/states/DL.py), [West Bengal](./data_extractor/bulletin_download/states/WB.py), and [Telangana](./data_extractor/bulletin_download/states/TG.py) for reference.
3. [`db`](./data_extractor/db) - Interface to the database, defining the tables and data insertion queries.
   - [`main.py`](./data_extractor/db/main.py) - Main interface to different state databases
   - [`DL.py`](./data_extractor/db/DL.py) - Delhi specific database interface (other states follow the same pattern). Each file defines the list of tables related to the state, and an insert query for the data.
3. [`local_extractor`](./data_extractor/local_extractor) - Defines the data extraction procedure from the health bulletins of each state.
   - [`main.py`](./data_extractor/local_extractor/main.py) - Main interface to the different state data extraction procedures
   - [`states`](./data_extractor/local_extractor/states) - Folder where all states data extraction scripts reside. Each script is initialized with the date and the report file path, and need to define an `extract` function which returns a dictionary of the extracted data.
   - [`utils`](./data_extractor/local_extractor/utils) - Stores commonly used utilities to be used across the data extraction scripts, such as, extracting tables from textual PDFs, standardizing date formats, etc.

## How to recreate the database locally

While you can conveniently download the up-to-date database from the following link [https://www.dropbox.com/s/hbe04q6vtzapdam/covid-india.db?dl=1](https://www.dropbox.com/s/hbe04q6vtzapdam/covid-india.db?dl=1), you can also run the entire routine locally to recreate the database from scratch.

Locally, follow these steps to recreate the db:

1. Ensure you have the dependencies defined in the [`requirements.txt`](./requirements.txt) installed. If not, run `pip3 install -r requirements.txt` to install these dependencies.
2. Change directory into the `data_extractor` directory
3. Execute the [`run.py`](./data_extractor/run.py) script as `python3 run.py --datadir DATADIR`
   - `--datadir` argument defines the local folder path to store the bulletins , metadata files, and the database.

## How to add new states to the pipeline

Refer to this [Wiki](https://github.com/IBM/covid19-india-data/wiki/Adding-a-new-state-to-the-data-extraction-pipeline) to integrate a new state to the pipeline.