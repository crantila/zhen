#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
