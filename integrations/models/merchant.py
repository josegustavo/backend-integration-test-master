# -*- coding: utf-8 -*-
from integrations.libs.api import Api
from integrations.models.model import Model


class Merchant(Model):

    can_be_deleted: bool
    can_be_updated: bool
    is_active: bool
    name: str

    _api = None
    _api_url = '/api/merchants'

    def get_values(self):
        if self.id:
            return {
                'can_be_deleted': self.can_be_deleted,
                'can_be_updated': self.can_be_updated,
                'id': self.id,
                'is_active': self.is_active,
                'name': self.name,
            }

    def search(self, name):
        result = self._api.get_data(self._api_url)
        if 'merchants' in result:
            for merchant in result['merchants']:
                if merchant['name'] == name:
                    self.init_fields(merchant)
                    return self

