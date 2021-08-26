#!/bin/bash

IBM_CLOUD_FRONTEND_SPACE="covid-19-data-india"

ibmcloud target -s ${IBM_CLOUD_FRONTEND_SPACE} -o ${IBM_CLOUD_ORG}

cd ${TRAVIS_BUILD_DIR}/frontend
yarn
yarn build
ibmcloud cf push