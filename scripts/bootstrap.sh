#!/usr/bin/env bash

MDBG_URL="http://www.mdbg.net/chindict/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz"

if [ -n "${OPENSHIFT_DATA_DIR+1}" ]; then
    CONVERSION_SCRIPT="${OPENSHIFT_REPO_DIR}scripts/mdbg_to_sqlite.py"
    MDBG_FILENAME="${OPENSHIFT_TMP_DIR}mdbg-`date +'%Y-%m-%d'`"
    DB_FILENAME="${OPENSHIFT_DATA_DIR}zhen_db.sqlite3"
else
    CONVERSION_SCRIPT="scripts/mdbg_to_sqlite.py"
    MDBG_FILENAME="mdbg-`date +'%Y-%m-%d'`"
    DB_FILENAME="zhen_db.sqlite3"
fi


echo "Downloading words database from MDBG"
curl ${MDBG_URL} -s -o "${MDBG_FILENAME}.gz"

echo "Unzipping database"
gunzip -f "${MDBG_FILENAME}.gz"

echo "Converting database for Zhen"
python3 ${CONVERSION_SCRIPT} ${MDBG_FILENAME} ${DB_FILENAME}
