#!/usr/bin/env python3

"""
OpenShift runs this script to start Zhen.

You may be able to use this script elsewhere, but "python -m zhen" is recommended when possible.
"""

import os
import sys

if 'OPENSHIFT_REPO_DIR' in os.environ:
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi',))
    virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/venv'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python3.3/site-packages')
    virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
    try:
        exec(compile(open(virtualenv).read(), virtualenv, 'exec'),dict(__file__ = virtualenv))
    except IOError:
        pass

import tornado.ioloop
import tornado.web
from zhen import handlers, lookup

if 'OPENSHIFT_REPO_DIR' in os.environ:
    settings = {'static_path' : os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'static')}
else:
    settings = {'static_path' : os.path.join(os.getcwd(), 'static')}

port = int(os.environ.get('OPENSHIFT_PYTHON_PORT', '8000'))
ip = os.environ.get('OPENSHIFT_PYTHON_IP', 'localhost')


from tornado import ioloop, web
from zhen import handlers, lookup


if __name__ == '__main__':
    print('Starting up from app.py!')
    lookup.load()
    app = web.Application(handlers.HANDLER_DEFINITIONS, debug=False, **settings)
    app.listen(port, ip)
    ioloop.IOLoop.current().start()
