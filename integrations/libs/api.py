# -*- coding: utf-8 -*-

import time
import requests

from integrations.tools.decorators import Decorators


class Api(object):

    token = {}

    def __init__(self, base_url: str = None, client_id: str = None, client_secret: str = None, grant_type: str = None):
        self._base_url = base_url

        self._credentials = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': grant_type,
        }

    def __get_url(self, url: str):
        return self._base_url + '/' + url.strip("/")

    def get_access_token(self):
        url = self.__get_url('/oauth/token')
        now = time.time()
        request = requests.post(url, params=self._credentials)
        response = request.json()
        if 'access_token' not in response:
            raise Exception(response.get('error', 'Invalid credentials'))
        token = response
        token['token_expiration'] = now + token['expires_in']
        return token

    def _get_headers(self):
        headers = {'token': 'Bearer ' + self.token.get('access_token')}
        return headers

    def send(self, url):
        pass

    @Decorators.ensure_token
    def get_data(self, url: str):
        r = requests.get(self.__get_url(url), headers=self._get_headers())
        if r.ok:
            return r.json()

    @Decorators.ensure_token
    def put_data(self, url, update):
        r = requests.put(self.__get_url(url), headers=self._get_headers(), json=update)
        if r.ok:
            return r.json()

    @Decorators.ensure_token
    def delete_data(self, url):
        r = requests.delete(self.__get_url(url), headers=self._get_headers())
        if r.ok:
            return True

    @Decorators.ensure_token
    @Decorators.limit_request(per_hour=2000, per_day=10000)
    def post_data(self, url, data):
        r = requests.post(self.__get_url(url), headers=self._get_headers(), json=data)
        print('Post product data', r.json())
        if r.ok:
            return r.json()