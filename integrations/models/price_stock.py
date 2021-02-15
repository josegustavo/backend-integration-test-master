# -*- coding: utf-8 -*-

from integrations.data_input.data_csv import DataCsv


class PriceStock(DataCsv):
    _columns = ['SKU', 'BRANCH', 'PRICE', 'STOCK']

    _index = 'SKU'
