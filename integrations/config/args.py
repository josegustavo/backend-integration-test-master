# -*- coding: utf-8 -*-
from argparse import ArgumentParser
from libs.config_source import ConfigSource


class Args(ConfigSource):

    _arguments = [{
        0: '-d',
        1: '--debug',
        'action': 'store_true',
        'default': False,
        'help': 'Print some debug information'
    }]

    def __init__(self):
        super(Args, self).__init__()
        self._parser = ArgumentParser(
            description='Process CSV files and then use the data to connect it to an "external" Ingestion API',
        )
        self._parser.add_argument('-d', '--debug', action="store_true", default=False, help='Print some debug information')
        self._parser.add_argument('-p', '--products-path', action="store", dest="products_path", type=str,
                            help='Path of the file PRODUCTS.csv', required=True)
        self._parser.add_argument('-s', '--price-stock-path', action="store", dest="price_stock_path", type=str,
                            help='Path of the file PRICES-STOCK.csv', required=True)

        self._values = self._parser.parse_args()
