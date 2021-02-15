# -*- coding: utf-8 -*-

from integrations.data_input.data_csv import DataCsv


class Product(DataCsv):

    _api_url = '/api/products'

    _merchant_id: str

    _columns = ['SKU', 'BUY_UNIT', 'DESCRIPTION_STATUS', 'ORGANIC_ITEM', 'KIRLAND_ITEM', 'FINELINE_NUMBER', 'EAN', 'ITEM_NAME', 'ITEM_DESCRIPTION', 'ITEM_IMG', 'CATEGORY', 'SUB_CATEGORY', 'SUB_SUB_CATEGORY', 'BRAND_NAME']

    _index = 'SKU'

    def __init__(self, merchant_id: str = None, *args, **kwargs):
        super(Product, self).__init__(*args, **kwargs)
        if merchant_id:
            self._merchant_id = merchant_id

    def load(self, product_data={}):
        # print(self.get_data().describe())

        product_data['merchant_id'] = self._merchant_id
        # result = self._api.post_data(self._api_url, product_data)

