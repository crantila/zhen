#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           zhen
# Program Description:    Web translation between ZHongwen and ENglish.
#
# Filename:               setup.py
# Purpose:                Configuration for installation with setuptools.
#
# Copyright (C) 2016 Christopher Antila
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#--------------------------------------------------------------------------------------------------
'''
Configuration for installation with setuptools.
'''

from setuptools import setup, Command


setup(
    name = 'Zhen',
    version = '0.0.1',
    packages = ['zhen'],

    install_requires = ['tornado==4.3', 'Jinja2<3'],
    tests_require = ['pytest<3'],

    author = 'Christopher Antila',
    author_email = 'christopher@antila.ca',
    description = '汉语-英语词典 Chinese-English Dictionary',
    # long_description = '???',
    license = 'AGPLv3+',
    keywords = 'translate,translation,dictionary,chinese,english,web app',
    url = 'https://github.com/crantila/zhen',
    classifiers =[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Programming Language :: Python :: 3.4',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Education',
        'Topic :: Text Processing :: Linguistic',
    ],
)
