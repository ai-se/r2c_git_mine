#!/bin/bash

set -e
CODE_DIR="/analysis/inputs/public/source-code"

SRC_CODE='/analyzer'

export PYTHONPATH=$PYTHONPATH:/analyzer/understand/scitools/bin/linux64/Python
export PATH=$PATH:/analyzer/understand/scitools/bin/linux64


cd ${SRC_CODE}

python3 /analyzer/get_metrices.py ${CODE_DIR}> /analysis/output/output.json