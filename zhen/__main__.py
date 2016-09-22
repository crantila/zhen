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

# TODO: choose simp/trad for classifiers
# TODO: remove the comma at the end of every English definition list

from jinja2 import Environment, PackageLoader
from tornado import ioloop, gen, template, web

from zhen import lookup


JINJA = Environment(  # TODO: make it SandboxedEnvironment?
    autoescape=True,  # TODO: change this to the "Autoescape Extension"
    auto_reload=True,  # DEBUG: only for debugging
    loader=PackageLoader('zhen', 'templates'),
    lstrip_blocks=True,  # TODO: this doesn't seem to work
    optimized=False,  # DEBUG: only for debugging
    trim_blocks=True,
)


def remove_spaces(spaced):
    """
    Filter unnecessary spaces from a rendered template.

    This is intended to run as a filter on a complete template. It removes:

    - blank lines
    - whitespace at the start of a line
    - whitespace at the end of a line
    """
    post = []
    for each_line in spaced.split('\n'):
        stripped = each_line.strip()
        if stripped:
            post.append(stripped)

    return '\n'.join(post)

JINJA.filters['remove_spaces'] = remove_spaces


def _verify_chars(chars):
    """
    Verify the "chars" query argument. If the parameter to this function is either `'s'` or `'t'`,
    it is returned; otherwise the default `'s'` is returned.
    """
    if chars == 't':
        return chars
    else:
        return 's'


class MainHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        chars = _verify_chars(self.get_argument('chars', 's'))
        self.write(JINJA.get_template('search.html').render(chars=chars))


class DefinitionHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.post()

    @gen.coroutine
    def post(self):
        word = self.get_argument('word')  # TODO: filter the word for safety
        chars = _verify_chars(self.get_argument('chars', 's'))
        results = lookup.find(word)
        self.write(JINJA.get_template('define.html').render(
            chars=chars,
            results=results,
            searched=word,
        ))


class CharactersHandler(web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.post()

    @gen.coroutine
    def post(self):
        word = self.get_argument('word')  # TODO: filter the word for safety
        chars = _verify_chars(self.get_argument('chars', 's'))
        results = []
        for each_char in word:
            results.extend(lookup.find_chinese(each_char))
        self.write(JINJA.get_template('characters.html').render(
            chars=chars,
            results=results,
            searched=word,
        ))


def make_app():
    return web.Application([
        (r'/', MainHandler),
        (r'/characters', CharactersHandler),
        (r'/define', DefinitionHandler),],
        debug=True)


if __name__ == '__main__':
    lookup.load()
    app = make_app()
    app.listen(8000)
    print('Go!')
    ioloop.IOLoop.current().start()
