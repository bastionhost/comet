#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado.options import define, options

define("port", default=8888, help="Run on the given port", type=int)
define("num_processes", default=1, help="Run the give num processes ", type=int)
define("is_debug", default=True, help="True if debug mode", type=bool)

options.logging = 'debug'
options.log_file_prefix = 'log/comet.log'
