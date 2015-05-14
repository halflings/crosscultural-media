import requests
import urllib
import socket

BASE_URL = 'https://ajax.googleapis.com/ajax/services/search/news'

class LinkEntry(object):
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def __str__(self):
        return self.link

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
            new_start = start

            for result in jsonResult["responseData"]["results"]:
                #Only add result in the target language
                if result["language"] == language:
                    results.append(LinkEntry(title=result["title"], link=result["unescapedUrl"]))
                new_start += 1

            return (results, new_start)
        else:
            return ([], start)

    # Fetches news articles
    def news(self, query, max_results, language=None):
        results = []
        start = 0

        while True:
            (temp_res, start) = self.fetch_news_at(query, start, language)

            # If we got back zero results, we have reached the end
            if len(temp_res) == 0:
                break

            # Append the returned results to the larger result
            for res in temp_res:
                results.append(res)

            if len(results) >= max_results:
                break

        return results

if __name__ == '__main__':
    api = GoogleNewsAPI()
    results = api.news('olja', 50, 'sv')
    for result in results:
        print result 