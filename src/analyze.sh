#!/bin/bash

set -e
CODE_DIR="/analysis/inputs/public/source-code"

SRC_CODE='/analyzer'


cd ${SRC_CODE}

python3 /analyzer/src/get_metrices.py ${CODE_DIR}> /analysis/output/output.json