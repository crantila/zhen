#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------------------------------------------------------------------------------
# Program Name:           Zhen
# Program Description:    Chinese-English Translating Dictionary
#
# Filename:               zhen/handlers.py
# Purpose:                Tornado request handlers.
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
Tornado request handlers.
"""

from jinja2 import Environment, PackageLoader
from tornado import gen, web

from zhen import lookup


if __debug__:
    jinja_auto_reload = True
    jinja_optimized = False
else:
    jinja_auto_reload = False
    jinja_optimized = True


JINJA = Environment(  # TODO: make it SandboxedEnvironment?
    autoescape=True,  # TODO: change this to the "Autoescape Extension"
    auto_reload=jinja_auto_reload,
    loader=PackageLoader('zhen', 'templates'),
    lstrip_blocks=True,
    optimized=jinja_optimized,
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

if __debug__:
    JINJA.filters['remove_spaces'] = lambda x: x
else:
    JINJA.filters['remove_spaces'] = remove_spaces


def request_wrapper(func):
    """
    Use this function as a decorator on a handler to prevent mysterious failures when an exception
    happens. This function calls :meth:`send_error`. If ```__debug__`` is ``True``, a traceback
    will be emitted with :func:`print`.

    .. note:: That the method being decorated is assumed to be a Tornado coroutine. You must put
        the ``@request_wrapper`` decorator *above* the coroutine decorator, like this:

        @request_wrapper
        @coroutine
        def get(self):
            pass
    """

    @gen.coroutine
    def decorated(self, *args, **kwargs):
        """Wraps."""
        try:
            yield func(self, *args, **kwargs)
        except (gen.BadYieldError, Exception) as exc:   # pylint: disable=broad-except
            if __debug__:
                if isinstance(exc, gen.BadYieldError):
                    print('IMPORTANT: write the @request_wrapper decorator above @gen.coroutine')
                else:
                    import traceback
                    traceback.print_exception(type(exc), exc, exc.__traceback__)

            self.send_error(500, reason='Programmer Error')

    return decorated


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
    @request_wrapper
    @gen.coroutine
    def get(self):
        chars = _verify_chars(self.get_argument('chars', 's'))
        self.write(JINJA.get_template('search.html').render(chars=chars))


class DefinitionHandler(web.RequestHandler):
    @request_wrapper
    @gen.coroutine
    def get(self):
        self.post()

    @request_wrapper
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
    @request_wrapper
    @gen.coroutine
    def get(self):
        self.post()

    @request_wrapper
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


HANDLER_DEFINITIONS = [
    (r'/', MainHandler),
    (r'/characters', CharactersHandler),
    (r'/define', DefinitionHandler),
]
