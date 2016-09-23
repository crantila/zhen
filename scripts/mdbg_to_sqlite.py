#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           Zhen
# Program Description:    Chinese-English Translating Dictionary
#
# Filename:               scripts/mdbg_to_sqlite.py
# Purpose:                Load the MDBG dictionary export into a SQLite3 database.
#
# Copyright (C) 2016 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
"""
Load the MDBG dictionary export into a SQLite3 database.
"""

import os
import os.path
import sqlite3
import sys


english_db = {'highest_id': 0}
# This is a mapping from English term to a two-term dict with "id" and "xref," containing the ID for
# the English term and a list of xref IDs for the corresponding Chinese words, respectively.


def init_db(database_path):
    """
    Create a new dictionary database. If the database file exists, delete it first.
    """
    # delete existing database
    if os.path.exists(database_path):
        os.unlink(database_path)

    # make new database
    conn = sqlite3.Connection(database_path)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE english (
        id INTEGER PRIMARY KEY,
        word TEXT,
        x_chinese TEXT);''')
    cur.execute('''CREATE TABLE chinese (
        id INTEGER PRIMARY KEY,
        classifier TEXT,
        simplified TEXT,
        traditional TEXT,
        pinyin TEXT,
        x_english TEXT);''')
    conn.commit()

    return conn


def english_maker(x_chinese, word):
    """
    Enter an English term to the database, returning its ID. If the term already exists in the
    database, the existing ID is returned.

    :param x_chinese: The cross-reference ID to use in the "x_chinese" database field.
    :type x_chinese: int or str
    :param str word: The English term to use in the "word" database field.
    :returns: The ID of the word the *exactly* matches "word" in the database, whether or not it
        already existed in the database.
    :rtype: str
    """
    global english_db

    if word in english_db:
        english_db[word]['xref'].append(str(x_chinese))

    else:
        english_db[word] = {'id': english_db['highest_id'] + 1, 'xref': [str(x_chinese)]}
        english_db['highest_id'] += 1

    return str(english_db[word]['id'])


def extractor(i, word, cur):
    post = {
        'c': '',  # for "classifier," which may not be filled
        'e': [],  # English translations
        's': None,  # the simplified character
        't': None,  # the traditional character
    }

    first_space_i = word.find(' ')
    # traditional
    post['t'] = word[:first_space_i]
    # simplified
    post['s'] = word[first_space_i+1 : word.find(' ', first_space_i+1)]
    # pinyin
    post['p'] = word[word.find('[')+1 : word.find(']')]
    # english/classifier
    definitions = word[word.find('/')+1:].split('/')[:-1]
    for definition in definitions:
        if definition.startswith('CL:'):
            definition = definition[3:]  # remove the 'CL:' prefix
            definition = definition[:definition.find('[')]  # also remove the pinyin
            post['c'] = definition
        else:
            post['e'].append(english_maker(i, definition))

    cur.execute(
        'INSERT INTO chinese (id, classifier, simplified, traditional, pinyin, x_english) VALUES (?,?,?,?,?,?)',
        (i, post['c'], post['s'], post['t'], post['p'], ','.join(post['e'])))


def add_the_english(cur):
    """
    Add the English terms to the database.
    """
    for word, val in english_db.items():
        if word == 'highest_id':
            continue
        cur.execute(
            'INSERT INTO english (id, word, x_chinese) VALUES (?,?,?)',
            (val['id'], word, ','.join(val['xref'])))


def main():
    if (sys.argv[0].endswith('.py') and len(sys.argv) < 3) or len(sys.argv) < 2:
        print('Usage: mdbg_to_sqlite.py MDBG_EXPORT_FILE DATABASE_PATH')
        raise SystemExit(1)

    if sys.argv[0].endswith('.py'):
        export_file = sys.argv[1]
        database_path = sys.argv[2]
    else:
        export_file = sys.argv[0]
        database_path = sys.argv[1]

    conn = init_db(database_path)
    with conn:
        with open(export_file, encoding='utf-8') as source:
            cur = conn.cursor()
            for i, each in enumerate(source):
                if each.startswith('#'):
                    continue
                extractor(i, each.strip(), cur)

            add_the_english(cur)


if __name__ == '__main__':
    main()
