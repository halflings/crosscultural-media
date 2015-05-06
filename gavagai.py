import requests

BASE_URL = 'https://api.gavagai.se/v3'
DEFAULT_HEADERS = {'Content-Type': 'application/json'}

class Gavagai(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self._auth_params = dict(apiKey=self.api_key)

    def _request(self, endpoint, payload):
        return requests.post('{}/{}'.format(BASE_URL, endpoint), headers=DEFAULT_HEADERS,
                             json=payload, params=self._auth_params, verify=False).json()

    def tonality(self, texts, language):
        texts_data = [dict(body=text, id=str(i)) for i, text in enumerate(texts)]
        data = dict(language=language, texts=texts_data)
        return self._request('tonality', data)