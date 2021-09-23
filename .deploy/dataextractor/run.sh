#!/bin/bash

CURR_DIR=`pwd`;
HOME_DIR=`realpath ../..`;
DATAEXTRACTOR_DIR="${HOME_DIR}/data_extractor"
LOCALSTORE_DIR="${HOME_DIR}/localstore"


# Install dropbox library
pip3 install dropbox
pip3 install -r "${DATAEXTRACTOR_DIR}/requirements.txt"

# Fetch the latest code from github
cd ${HOME_DIR}
git checkout main
git pull origin main


# Run the data extractor
cd ${DATAEXTRACTOR_DIR}
python3 run.py --datadir "${LOCALSTORE_DIR}"

# Upload the new database to dropbox
DB_PATH="${LOCALSTORE_DIR}/covid-india.db"
cd "${CURR_DIR}"

python3 upload_to_dropbox.py "${DB_PATH}"