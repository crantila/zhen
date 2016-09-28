#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           Zhen
# Program Description:    Chinese-English Translating Dictionary
#
# Filename:               zhen/lookup.py
# Purpose:                Search for a word.
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

import os
import os.path
import sqlite3


DATABASE_FILENAME = 'zhen_db.sqlite3'
_DB = None


def load():
    """
    Load the SQLite database.
    """
    global _DB

    if 'OPENSHIFT_DATA_DIR' in os.environ:
        db_file = os.path.join(os.environ['OPENSHIFT_DATA_DIR'], DATABASE_FILENAME)
    else:
        # db_file = pathlib.Path(__file__).parent.parent.joinpath(DATABASE_FILENAME)
        db_file = os.path.join(os.path.split(os.path.split(__file__)[0])[0], DATABASE_FILENAME)

    if not os.path.exists(db_file) or not os.path.isfile(db_file):
        raise SystemExit(32)

    _DB = sqlite3.Connection(str(db_file))


def _format_chinese(cur):
    """
    Format the result of database query on the "chinese" table.

    :param cur: A :class:`sqlite3.Cursor` that just ran a query.
    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict

    In the cursor results, we assume the following fields:

    - 0: id
    - 1: classifier
    - 2: simplified
    - 3: traditional
    - 4: pinyin

    Formatting is done by first cross-referencing the English definitions, then by filling in all
    the fields to a dictionary with the following keys:

    - c: classifier
    - s: simplified Chinese
    - t: traditional Chinese
    - p: pinyin
    - e: English
    """
    post = []
    for chinese in cur:
        subcur = _DB.execute('''
            SELECT word FROM english
                WHERE id IN (SELECT english_id FROM definitions WHERE chinese_id=?);
            ''',
            (chinese[0],))
        english = [x[0] for x in subcur]

        post.append({
            'c': chinese[1],
            's': chinese[2],
            't': chinese[3],
            'p': chinese[4],
            'e': english,
        })

    return post


def find_simplified(word):
    """
    Find a word by simplified characters.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    cur = _DB.execute(
        'SELECT id, classifier, simplified, traditional, pinyin FROM chinese WHERE simplified=?',
        (word,))

    return _format_chinese(cur)


def find_traditional(word):
    """
    Find a word by traditional characters.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    cur = _DB.execute(
        'SELECT id, classifier, simplified, traditional, pinyin FROM chinese WHERE traditional=?',
        (word,))

    return _format_chinese(cur)


def find_pinyin(word):
    """
    Find a word by pinyin.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    word = word.lower()

    cur = _DB.execute(
        'SELECT id, classifier, simplified, traditional, pinyin FROM chinese WHERE pinyin=?',
        (word,))

    return _format_chinese(cur)


def find_english(word):
    """
    Find an English word.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    word = word.lower()

    cur = _DB.execute('''
        SELECT id, classifier, simplified, traditional, pinyin FROM chinese
            WHERE id IN (SELECT chinese_id FROM definitions
                WHERE english_id in (SELECT id FROM english WHERE word_lowercase=?
        ));''',
        (word,))

    return _format_chinese(cur)


def find_chinese(characters):
    """
    Find a word in Chinese characters only.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    post = find_simplified(characters)
    if post:
        return post

    post = find_traditional(characters)
    if post:
        return post

    return []


def find(word):
    """
    Try to find a word at any cost.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict

    The search order is:

    - simplified
    - traditional
    - English
    - pinyin
    """
    post = find_simplified(word)
    if post:
        return post

    post = find_traditional(word)
    if post:
        return post

    post = find_english(word)
    if post:
        return post

    post = find_pinyin(word)
    if post:
        return post

    return []
