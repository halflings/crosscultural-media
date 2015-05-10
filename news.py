#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

import feedparser
import socket

BASE_URL = 'https://news.google.com'

class GoogleNews(object):
    def __init__(self, userip=None):
        self.userip = userip or socket.gethostbyname(socket.gethostname())

    def news(self, query, language=None):
        params = dict(q=unicode(query).encode('utf-8'), output='rss', userip=self.userip)
        if language:
            # params['ned'] = language
            params['hl'] = language # Using 'hl' seems to give the results in the target language
        query_string = u'{}?{}'.format(BASE_URL, urllib.urlencode(params))
        feed = feedparser.parse(query_string)
        return feed.entries