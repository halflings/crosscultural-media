import feedparser
import socket

BASE_URL = 'https://news.google.com'

class GoogleNews(object):
    def __init__(self, userip=None):
        self.userip = userip or socket.gethostbyname(socket.gethostname())

    def news(self, query, language=None):
        params = dict(q=query, output='rss', userip=self.userip)
        if language:
            params['ned'] = language
        encoded_params = '&'.join(u'{}={}'.format(key, value) for key, value in params.iteritems())
        query_string = u'{}?{}'.format(BASE_URL, encoded_params)
        print query_string
        feed = feedparser.parse(query_string)
        return feed.entries