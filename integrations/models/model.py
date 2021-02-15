# -*- coding: utf-8 -*-
from integrations.libs.api import Api


class Model(object):

    id: str

    _api_url: str
    _api = None

    def __init__(self, api_request: Api=None, **kwargs):
        if api_request:
            self._api = api_request
        if kwargs:
            self.init_fields(kwargs)

    def get_values(self):
        raise NotImplementedError

    def init_fields(self, items={}):
        if not items:
            return
        for item, value in items.items():
            setattr(self, item, value)

    def search(self):
        raise NotImplementedError

    def update(self, **kwargs):
        url = self._api_url + '/' + self.id

        for k, v in kwargs.items():
            setattr(self, k, v)

        result = self._api.put_data(url, self.get_values())
        if result.get('id') == self.id:
            return True

    def remove(self):
        url = self._api_url + '/' + self.id
        return self._api.delete_data(url)
