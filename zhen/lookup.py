#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
