#-*- coding: utf-8 -*-

import config

from tornado import web
from tornado import httpserver
from tornado import ioloop
from tornado.options import options

from urls import handlers

def run():
    application = web.Application(handlers)
    http_server = httpserver.HTTPServer(application, xheaders=True)
    http_server.bind(options.port)
    http_server.start(options.num_processes)
    loop = ioloop.IOLoop.instance()
    loop.start()

if __name__ == "__main__":
    run()
