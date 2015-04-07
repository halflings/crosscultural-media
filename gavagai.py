import requests

BASE_URL = 'https://api.gavagai.se/v3'
DEFAULT_HEADERS = {'Content-Type': 'application/json'}

class Gavagai(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self._auth_params = dict(apiKey=self.api_key)

    def _request(self, endpoint, payload):
        return requests.post('{}/{}'.format(BASE_URL, endpoint), headers=DEFAULT_HEADERS,
                             json=payload, params=self._auth_params).json()

    def tonality(self, texts, language):
        data = dict(language=language, texts=texts)
        return self._request('tonality', data)

if __name__ == '__main__':
    import config
    api = Gavagai(config.API_KEY)
    texts = [dict(body="angry text example, I hate you, blah blah.", id="randomtext")]
    print api.tonality(texts, "en")