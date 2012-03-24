#-*- coding: utf-8 -*-

from views import ConnectHandler
from views import UpdateHandler

handlers = [
    (r"/connect", ConnectHandler),
    (r"/update", UpdateHandler),
]
