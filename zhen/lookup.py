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

import pathlib
import sqlite3


DATABASE_FILENAME = 'zhen_db.sqlite3'
_DB = None


def load():
    """
    Load the SQLite database.
    """
    global _DB

    db_file = pathlib.Path(__file__).parent.parent.joinpath(DATABASE_FILENAME)
    if not db_file.exists() or not db_file.is_file():
        raise SystemExit(32)
    _DB = sqlite3.Connection(str(db_file))


def _format_chinese(cur):
    """
    Format the result of database query on the "chinese" table.

    :param cur: A :class:`sqlite3.Cursor` that just ran a query.
    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict

    Formatting is done by first cross-referencing the English definitions, then by filling in all
    the fields to a dictionary with the following keys:

    - c: classifier
    - s: simplified Chinese
    - t: traditional Chinese
    - p: pinyin
    - e: English
    """
    post = []
    for chinese in cur.fetchall():
        english = []
        for x_eng in chinese[4].split(','):
            for eng in _DB.execute('SELECT word FROM english WHERE id=?', (x_eng,)).fetchall():
                english.append(eng[0])

        post.append({
            'c': chinese[0],
            's': chinese[1],
            't': chinese[2],
            'p': chinese[3],
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
        'SELECT classifier, simplified, traditional, pinyin, x_english FROM chinese WHERE simplified=?',
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
        'SELECT classifier, simplified, traditional, pinyin, x_english FROM chinese WHERE traditional=?',
        (word,))

    return _format_chinese(cur)


def find_pinyin(word):
    """
    Find a word by pinyin.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    cur = _DB.execute(
        'SELECT classifier, simplified, traditional, pinyin, x_english FROM chinese WHERE pinyin=?',
        (word,))

    return _format_chinese(cur)


def find_english(word):
    """
    Find an English word.

    :param str word: The word to look up.
    :returns: A list of definition dictionaries.
    :rtype: list of dict
    """
    cur = _DB.execute(
        'SELECT x_chinese FROM english WHERE word=?',
        (word,))

    post = []
    for x_chin in cur.fetchall():
        for chin_id in x_chin[0].split(','):
            post.extend(_format_chinese(_DB.execute(
                'SELECT classifier, simplified, traditional, pinyin, x_english FROM chinese WHERE id=?',
                (chin_id,))))

    return post


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
