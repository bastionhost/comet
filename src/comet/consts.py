#!/usr/bin/env python
# -*- coding: utf-8 -*-

LIVE_ONLINE_USER_KEY            = 'live:online_users'
LIVE_CHANNEL_KEY_TMPL           = 'live:chn:{uid}:{event}'
LIVE_SINGLE_CHANNEL_KEY_TMPL    = 'live:single:{uid}:{event}'
LIVE_WILDCARD                   = 'live:*:{uid}:*'
LIVE_SINGLE_KEY_STORE           = 'live:store:single:{key}'

POLL_TIME = 2
CHANNEL_EXPIRE_TIME = 180 

FEED_ITEM_TTL = 5 * 60  # 5 minutes time to live before the item should be
                        # garbage collected
