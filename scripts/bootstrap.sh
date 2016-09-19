#!/usr/bin/env bash

MDBG_URL="http://www.mdbg.net/chindict/export/cedict/cedict_1_0_ts_utf-8_mdbg.txt.gz"
MDBG_FILENAME="mdbg-`date +'%Y-%m-%d'`"
DB_FILENAME="zhen_db.sqlite3"


echo "Downloading words database from MDBG"
curl ${MDBG_URL} -s -o "${MDBG_FILENAME}.gz"

echo "Unzipping database"
gunzip "${MDBG_FILENAME}.gz"

echo "Converting database for Zhen"
python3 scripts/mdbg_to_sqlite.py ${MDBG_FILENAME} ${DB_FILENAME}
