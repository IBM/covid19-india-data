#!/bin/bash

set -eux

CURR_FILEPATH=`realpath $0`
CURR_DIR=`dirname ${CURR_FILEPATH}`;
HOME_DIR=`realpath ${CURR_DIR}/../..`;
TABNET_DIR="${HOME_DIR}/tabnet_model"

# Install TabNet dependencies
pip install torch==1.5.1+cpu torchvision==0.6.1+cpu -f https://download.pytorch.org/whl/torch_stable.html
pip install mmcv-full==1.0.5 -f https://download.openmmlab.com/mmcv/dist/cpu/torch1.5.0/index.html
pip install mmdet==2.3.0
pip install Wand pycocotools PyPDF2

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