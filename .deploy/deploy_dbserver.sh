#!/bin/bash

IBM_CLOUD_DBSERVER_SPACE="covid-19-data-india-storage"

ibmcloud target -s ${IBM_CLOUD_DBSERVER_SPACE} -o ${IBM_CLOUD_ORG}
cd ${TRAVIS_BUILD_DIR}/serve_db

# Download latest DB from the source folder
curl -L -o "./covid-india.db" "https://www.dropbox.com/s/hbe04q6vtzapdam/covid-india.db?dl=1"

# Push and deploy to IBM Cloud
ibmcloud cf push