import feedparser
import socket
import urllib

BASE_URL = 'https://news.google.com'

class GoogleNews(object):
    def __init__(self, userip=None):
        self.userip = userip or socket.gethostbyname(socket.gethostname())

    def news(self, query, language=None):
        params = dict(q=query, output='rss', userip=self.userip)
        if language:
            params['ned'] = language
        query_string = '{}?{}'.format(BASE_URL, urllib.urlencode(params))
        feed = feedparser.parse(query_string)
        return feed.entries

news_api = GoogleNews()
results = news_api.news("kaffe", "sv")