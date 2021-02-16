# -*- coding: utf-8 -*-
import unittest
from unittest.mock import Mock, patch

from integrations.libs.api import Api
from integrations.models.merchant import Merchant


class MerchantTestCase(unittest.TestCase):
    response_merchants = {'merchants': [
        {'name': 'One Merchant', 'id': '1111111'},
        {'name': 'Two Merchant', 'id': '2222222'},
        {'name': 'Some Merchant', 'id': '333333'},
        {'name': 'Another Merchant', 'id': '444'},
    ]}

    token = {'access_token': 'xxxxxxx'}

    api = Api('base_url', 'client_id,', 'client_secret', 'grant_type')

    @patch('integrations.libs.api.requests.get')
    @patch('integrations.libs.api.Api.get_access_token')
    def test_getting_merchant_ok(self, mock_access_token, mock_get):
        mock_access_token.return_value = self.token

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.response_merchants

        merchant = Merchant(api_request=self.api).search("Some Merchant")

        assert merchant.name == 'Some Merchant'

    @patch('integrations.libs.api.requests.get')
    @patch('integrations.libs.api.Api.get_access_token')
    def test_getting_merchant_not_ok(self, mock_access_token, mock_get):
        mock_access_token.return_value = self.token

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.response_merchants

        merchant = Merchant(api_request=self.api).search("Last Merchant")

        assert merchant is None

    @patch('integrations.libs.api.requests.get')
    @patch('integrations.libs.api.requests.put')
    @patch('integrations.libs.api.Api.get_access_token')
    def test_updating_merchant_ok(self, mock_access_token, mock_put, mock_get):
        mock_access_token.return_value = self.token

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.response_merchants

        mock_put.return_value = Mock(ok=True)
        mock_put.return_value.json.return_value = self.response_merchants['merchants'][2]

        merchant = Merchant(api_request=self.api).search("Some Merchant")

        assert merchant.update(**self.response_merchants['merchants'][2])

    @patch('integrations.libs.api.requests.get')
    @patch('integrations.libs.api.requests.put')
    @patch('integrations.libs.api.Api.get_access_token')
    def test_updating_merchant_not_ok(self, mock_access_token, mock_put, mock_get):
        mock_access_token.return_value = self.token

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.response_merchants

        mock_put.return_value = Mock(ok=True)
        mock_put.return_value.json.return_value = self.response_merchants['merchants'][1]

        merchant = Merchant(api_request=self.api).search("Two Merchant")

        assert not merchant.update(**self.response_merchants['merchants'][2])

    @patch('integrations.libs.api.requests.get')
    @patch('integrations.libs.api.requests.delete')
    @patch('integrations.libs.api.Api.get_access_token')
    def test_deleting_merchant_ok(self, mock_access_token, mock_delete, mock_get):
        mock_access_token.return_value = self.token

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.response_merchants

        mock_delete.return_value = Mock(ok=True)

        merchant = Merchant(api_request=self.api).search("Some Merchant")

        assert merchant.remove()

    @patch('integrations.libs.api.requests.get')
    @patch('integrations.libs.api.requests.delete')
    @patch('integrations.libs.api.Api.get_access_token')
    def test_deleting_merchant_not_ok(self, mock_access_token, mock_delete, mock_get):
        mock_access_token.return_value = self.token

        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.json.return_value = self.response_merchants

        mock_delete.return_value = Mock(ok=False)

        merchant = Merchant(api_request=self.api).search("Some Merchant")

        assert not merchant.remove()
