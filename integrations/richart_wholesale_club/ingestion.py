# -*- coding: utf-8 -*-
from libs.config_source import ConfigSource
from models.price_stock import PriceStock
from models.product import Product


class Ingestion:

    _config: ConfigSource = None

    def __init__(self, config: ConfigSource):
        self._config = config

    def process_csv_files(self):
        products = Product(self._config.products_path)
        price_stock = PriceStock(self._config.price_stock_path)

    def extract(self):
        pass

    def transform(self):
        pass

    def load(self):
        pass

