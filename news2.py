import requests
import urllib
import socket

BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/news'

class GoogleNewsAPI(object):
    def __init__(self, userip=None):
        self.userip = userip or socket.gethostbyname(socket.gethostname())

    # Fetches news articles starting at the given offset
    def fetch_news_at(self, query, start, language):
        # Build the request
        params = dict(q=unicode(query).encode('utf-8'), v="1.0", hl=language, start=start, userip=self.userip)
        query_string = u'{}?{}'.format(BASE_URL, urllib.urlencode(params))
        jsonResult = requests.get(query_string).json()

        # Check the result (we might get out of range)
        if jsonResult["responseStatus"] == 200:
            results = []

            for result in jsonResult["responseData"]["results"]:
                results.append(result["unescapedUrl"]) 

            return results
        else:
            return []

    # Fetches news articles
    def news(self, query, max_results, language=None):
        results = []
        start = 0

        while True:
            temp_res = self.fetch_news_at(query, start, language)

            # If we got back zero results, we have reached the end
            if len(temp_res) == 0:
                break

            # Append the returned results to the larger result
            for res in temp_res:
                results.append(res)

            start += len(temp_res)

            if len(results) >= max_results:
                break

        return results

if __name__ == '__main__':
    api = GoogleNewsAPI()
    for result in api.news('coffee', 15):
        print result 