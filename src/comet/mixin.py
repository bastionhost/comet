#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
import time
import json
from zlib import decompress
import tornado
from redis import Redis
from tornado.options import options

import consts
from utils import millisec

class CometMixin(object):
    _single_keys = set()
    _normal_keys = set()
    redis = Redis(host=options.redis_host,port=options.redis_port,db=options.redis_db)

    def wait_for_data(self, uid, events, timestamp, callback, timeout):
        if timeout > 0:
            data, ts = self.fetch(uid, events, timestamp)
            if not data:
                tornado.ioloop.IOLoop.instance().add_timeout(time.time() + consts.POLL_TIME,
                    lambda: self.wait_for_data(uid, events, timestamp, callback, timeout - consts.POLL_TIME))
            else:
                callback(data, ts)
        else:
            callback([], millisec())

    def keep_alive(self, uid):
        self.redis.zadd(consts.LIVE_ONLINE_USER_KEY, int(uid), millisec())

    def channel_key(self, uid, event):
        return consts.LIVE_CHANNEL_KEY_TMPL.format(uid=uid, event=event)

    def is_single_key(self, uid, event):
        cls = CometMixin
        if event in cls._single_keys:
            return True
        if event in cls._normal_keys:
            return False
        single_key = consts.LIVE_SINGLE_CHANNEL_KEY_TMPL.format(uid=uid, event=event)
        if self.redis.exists(single_key):
            cls._single_keys.add(event)
            return True
        normal_key = consts.LIVE_CHANNEL_KEY_TMPL.format(uid=uid, event=event)
        if self.redis.exists(normal_key):
            cls._normal_keys.add(event)
            return False
        return False

    def fetch(self, uid, events, last_atime):
        timestamp = 0
        results = []
        for event in events:
            if self.is_single_key(uid, event):
                single_key = consts.LIVE_SINGLE_CHANNEL_KEY_TMPL.format(uid=uid, event=event)
                ctime = int(self.redis.hget(single_key, 'ctime') or 0)
                if ctime > last_atime:
                    data = json.loads(decompress(self.redis.hget(single_key, 'data')))
                    results.append(data)
                    timestamp = max(timestamp, ctime)
            else:
                zipped_data = self.redis.zrangebyscore(self.channel_key(uid, event), '({0}'.format(last_atime),
                    millisec(), withscores=True)
                if len(zipped_data) > 0:
                    max_ctime = zipped_data[-1][-1]
                    timestamp = max(timestamp, max_ctime)
                    results.extend([json.loads(decompress(value)) for (value, _) in zipped_data])
        timestamp = timestamp or millisec()
        return results, timestamp

    def get_single_store(self, key):
        single_key = consts.LIVE_SINGLE_KEY_STORE.format(key=key)
        return self.redis.get(single_key)
