# -*- coding: utf-8 -*-

import time
import requests

from integrations.libs.config_source import ConfigSource
from integrations.tools.decorators import Decorators


class Api(object):
    _config: ConfigSource = None

    token = {}

    def __init__(self, config: ConfigSource):
        self._config = config
        self._base_url = config.base_url

        self._credentials = {
            'client_id': config.client_id,
            'client_secret': config.client_secret,
            'grant_type': config.grant_type,
        }

    def __get_url(self, url: str):
        return self._base_url + '/' + url.strip("/")

    def get_access_token(self):
        if not self.token:
            url = self.__get_url('/oauth/token')
            now = time.time()
            request = requests.post(url, params=self._credentials)
            response = request.json()
            if 'access_token' not in response:
                raise Exception(response.get('error', 'Invalid credentials'))
            self.token = response
            self.token['token_expiration'] = now + self.token['expires_in']

    def _get_headers(self):
        headers = {'token': 'Bearer ' + self.token.get('access_token')}
        return headers

    def send(self, url):
        pass

    @Decorators.ensure_token
    def get_data(self, url: str):
        r = requests.get(self.__get_url(url), headers=self._get_headers())
        if r.status_code == requests.codes.ok:
            return r.json()

    @Decorators.ensure_token
    def put_data(self, url, update):
        r = requests.put(self.__get_url(url), headers=self._get_headers(), json=update)
        if r.status_code == requests.codes.ok:
            return r.json()

    @Decorators.ensure_token
    def delete_data(self, url):
        r = requests.delete(self.__get_url(url), headers=self._get_headers())
        if r.status_code == requests.codes.ok:
            return True

    @Decorators.ensure_token
    def post_data(self, url, data):
        r = requests.post(self.__get_url(url), headers=self._get_headers(), json=data)
        if r.status_code == requests.codes.ok:
            return r.json()