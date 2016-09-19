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

import json

OUTPUT_FILE = 'output.json'

_words = []


def load():
    global _words
    with open(OUTPUT_FILE) as outfile:
        _words = json.load(outfile)

def find_in_field(word, field):
    post = []

    if field == 'e':
        for each_word in _words:
            for each_english in each_word['e']:
                if each_english == word:
                    post.append(each_word)

    else:
        for each_word in _words:
            if each_word[field] == word:
                post.append(each_word)

    return post

def find_simplified(word):
    return find_in_field(word, 's')

def find_traditional(word):
    return find_in_field(word, 't')

def find_pinyin(word):
    return find_in_field(word, 'p')

def find_english(word):
    return find_in_field(word, 'e')


def find_chinese(word):
    """
    Only search for a word in traditional or simplified characters.
    """
    post = find_simplified(word)
    if post:
        return post

    post = find_traditional(word)
    if post:
        return post

    return []


def find(word):
    post = find_simplified(word)
    if post:
        return post

    post = find_traditional(word)
    if post:
        return post

    post = find_pinyin(word)
    if post:
        return post

    post = find_english(word)
    if post:
        return post

    return []
