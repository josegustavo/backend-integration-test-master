# -*- coding: utf-8 -*-
from argparse import ArgumentParser, SUPPRESS
from integrations.libs.config_source import ConfigSource


class Args(ConfigSource):

    def __init__(self):
        super(Args, self).__init__()
        self._parser = ArgumentParser(
            description='Process CSV files and then use the data to connect it to an "external" Ingestion API',
            argument_default=SUPPRESS
        )
        self._parser.add_argument('-d', '--debug', action="store_true", default=False, help='Print some debug information')

        self._parser.add_argument('-p', '--products-path', action="store", dest="products_path", type=str,
                            help='Path of the file PRODUCTS.csv', required=False)

        self._parser.add_argument('-s', '--price-stock-path', action="store", dest="price_stock_path", type=str,
                            help='Path of the file PRICES-STOCK.csv', required=False)

        self._parser.add_argument('-c', '--client-id', action="store", dest="client_id", type=str,
                                  help='Client ID', required=False)

        self._parser.add_argument('-k', '--client-secret', action="store", dest="client_secret", type=str,
                                  help='Client Secret', required=False)

        values = vars(self._parser.parse_args())
        self.set_values(values)
