#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           Zhen
# Program Description:    Chinese-English Translating Dictionary
#
# Filename:               zhen/__main__.py
# Purpose:                Start up Zhen.
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
Run Zhen as a native Tornado application.
"""

import os.path
from tornado import ioloop, web
from zhen import handlers, lookup


if __name__ == '__main__':
    lookup.load()
    app = web.Application(
        debug=__debug__,
        handlers=handlers.HANDLER_DEFINITIONS,
        static_path=os.path.join(os.path.split(os.path.split(__file__)[0])[0], 'static'),
    )
    app.listen(8000)
    print('Zhen is ready!')
    if __debug__:
        print('DEBUG mode')

    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        print('\nZhen is shutting down')
