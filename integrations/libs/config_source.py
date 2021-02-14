# -*- coding: utf-8 -*-

class ConfigSource(object):

    _persist_methods = [
        'products_path',
        'price_stock_path'
    ]
    _values = {}

    def __getattr__(self, attribute):
        if attribute in self._values:
            return getattr(self._values, attribute)
