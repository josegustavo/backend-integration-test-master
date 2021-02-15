# -*- coding: utf-8 -*-
import os


class ConfigSource(object):

    _keys = [
        'products_path',
        'price_stock_path',

        'base_url',
        'client_id',
        'client_secret',
        'grant_type',

        'allowed_branchs',
    ]

    # Default values
    _values = dict(
        # products_path=os.environ.get('PRODUCTS_PATH', 'https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/PRODUCTS.csv'),
        products_path=os.environ.get('PRODUCTS_PATH', 'D:\joseg\Downloads\PRODUCTS.csv'),
        # price_stock_path=os.environ.get('PRICE_STOCK_PATH', 'https://cornershop-scrapers-evaluation.s3.amazonaws.com/public/PRICES-STOCK.csv'),
        price_stock_path=os.environ.get('PRICE_STOCK_PATH', 'D:\joseg\Downloads\PRICES-STOCK.csv'),

        base_url=os.environ.get("BASE_URL", 'http://127.0.0.1:5000'),
        grant_type=os.environ.get("GRANT_TYPE", 'client_credentials'),
        client_id=os.environ.get("CLIENT_ID"),
        client_secret=os.environ.get("CLIENT_SECRET"),

        allowed_branchs=os.environ.get("ALLOWED_BRANCHS", 'MM,RHSM'),
    )

    def set_values(self, values):
        self._values.update(values)

    def get_allowed_branchs(self):
        return self._values.get('allowed_branchs').split(',')

    def __getattr__(self, item):
        if item in self._keys:
            return self._values.get(item)

