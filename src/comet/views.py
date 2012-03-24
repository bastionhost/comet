#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
import json
import tornado.web

from utils import millisec
from mixin import CometMixin

class CometHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        uid = self.get_secure_cookie("uid")
        if not uid:
            return None
        else:
            return int(uid)


class UpdateHandler(CometHandler, CometMixin):
    """
    Long-polling from browsers to servers
    """

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        try:
            timeout = int(self.get_argument('timeout', 30))
            timestamp = int(self.get_argument('timestamp', millisec()))
        except ValueError:
            # In case of error parsing int
            timeout = 30
            timestamp = millisec()
        uid = self.current_user.id
        events = self.get_argument('events', '').split(',')
        self.keep_alive(uid=uid)
        self.wait_for_data(uid, events, timestamp=timestamp, callback=self.async_callback(self.send_response),
            timeout=timeout)

    def send_response(self, data, timestamp=None):
        """
        Send response to the browser
        """
        timestamp = timestamp or millisec()
        callback = self.get_argument('callback')
        if not self.request.connection.stream.closed() and not self._finished:
            self.set_header('Content-Type', 'text/javascript;charset=UTF-8')
            js_version = self.get_single_store('js_version') or 0
            results = json.dumps([data, int(js_version), timestamp])
            self.finish('{callback}({data})'.format(callback=callback, data=results))

    def on_connection_close(self):
        """
        Browsers close connections
        """
        self.send_response(data='[]')

    def post(self, *args, **kwargs):
        """
        For closure testing only
        """
        self.write('testing update post')


class ConnectHandler(CometHandler):
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        """
        For closure testing only
        """
        self.write('testing connect get')
