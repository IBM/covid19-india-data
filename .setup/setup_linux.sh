#!/bin/bash

CURR_FILEPATH=`realpath $0`
CURR_DIR=`dirname ${CURR_FILEPATH}`;
HOME_DIR=`realpath ${CURR_DIR}/..`;
DATAEXTRACTOR_DIR="${HOME_DIR}/data_extractor"
TABNET_DIR="${HOME_DIR}/tabnet_model"


echo `which pip3`
echo `which python3`


# Install dependencies of python packages
echo "Installing 'ghostscript' and 'tcl-tk' for camelot python package"
echo "We might require sudo access for this"
sudo apt-get install ghostscript python3-tk
java --version

if [ $? -ne 0 ]
then
    echo "ERROR: Java Runtime not found on the system. Please install it to make 'tabula' package working"
fi

# Install native dependencies
python3 -m pip install -r "${DATAEXTRACTOR_DIR}/requirements.txt"


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


echo "============================================================================"
echo "  Add the following lines to your ~/.bashrc or ~/.bash_profile files"
echo "  These variables set path to TabNet model and config files to be used"
echo "  later by the data extractor"
echo "============================================================================"
echo ""
echo "export TABNET_CONFIGPATH=\"${TABNET_CONFIGPATH}\""
echo "export TABNET_MODELMATH=\"${TABNET_MODELPATH}\""