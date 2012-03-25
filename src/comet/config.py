#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.options import define, options

define("port", default=8888, help="Run on the given port", type=int)
define("num_processes", default=1, help="Run the give num processes ", type=int)
define("is_debug", default=True, help="True if debug mode", type=bool)

define("redis_host", default='127.0.0.1', help="Redis server")
define("redis_port", default=6379, help="Redis port")
define("redis_db", default=0, help="Redis db")

options.logging = 'debug'
options.log_file_prefix = 'log/comet.log'
