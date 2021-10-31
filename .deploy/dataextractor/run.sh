#!/bin/bash

set -eux

CURR_FILEPATH=`realpath $0`
CURR_DIR=`dirname ${CURR_FILEPATH}`;
HOME_DIR=`realpath ${CURR_DIR}/../..`;
DATAEXTRACTOR_DIR="${HOME_DIR}/data_extractor"
LOCALSTORE_DIR="${HOME_DIR}/localstore"
TABNET_DIR="${HOME_DIR}/tabnet_model"


conda activate covid
which pip3
which python3

# Install dropbox library
pip3 install dropbox
pip3 install -r "${DATAEXTRACTOR_DIR}/requirements.txt"

# Fetch the latest code from github
cd ${HOME_DIR}
git checkout main
git pull origin main

# Setup TabNet

# Install TabNet dependencies
pip install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install mmcv-full==1.0.5 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.5.0/index.html
pip install mmdet==2.3.0
pip install Wand pycocotools PyPDF2

# Install pdfplumber
# Cannot install through requirements file because of a version conflict with pdfminer
# Need to use the upgrade option to ensure PDFs are read correctly
pip install pdfplumber --upgrade

# Download tabnet configuration and model
export TABNET_CONFIGPATH="${TABNET_DIR}/config.py"
export TABNET_MODELPATH="${TABNET_DIR}/general_model.pth"

mkdir -p "${TABNET_DIR}"

if [ ! -f "${TABNET_CONFIGPATH}" ]; then
    wget -O "${TABNET_CONFIGPATH}" "https://raw.githubusercontent.com/iiLaurens/CascadeTabNet/mmdet2x/Config/cascade_mask_rcnn_hrnetv2p_w32_20e.py"
fi

if [ ! -f "${TABNET_MODELPATH}" ]; then
    wget -O "${TABNET_MODELPATH}" "https://github.com/iiLaurens/CascadeTabNet/releases/download/v1.0.0/General.Model.table.detection.v2.pth"
fi


# Run the data extractor
cd ${DATAEXTRACTOR_DIR}
python3 run.py --datadir "${LOCALSTORE_DIR}"

# Upload the new database to dropbox
DB_PATH="${LOCALSTORE_DIR}/covid-india.db"
cd "${CURR_DIR}"

python3 upload_to_dropbox.py "${DB_PATH}"
