# -*- coding: utf-8 -*-
from integrations.libs.api import Api
from integrations.libs.config_source import ConfigSource
from integrations.models.merchant import Merchant
from integrations.models.price_stock import PriceStock
from integrations.models.product import Product
from integrations.transforms.branch_filter import BranchFilter
from integrations.transforms.categories_join import CategoriesJoin
from integrations.transforms.package_extract import PackageExtract
from integrations.transforms.sku_unique import SkuUnique
from integrations.transforms.stock_positive import StockPositive
from integrations.transforms.text_clean import TextClean
from integrations.transforms.transform import Transforms
import pandas as pd

class Ingestion:
    _config: ConfigSource = None
    _products = None
    _price_stock = None
    _api = None
    _richards = None

    def __init__(self, config: ConfigSource):
        self._config = config
        self._api = Api(self._config)

    def process_csv_files(self):
        self.extract()
        self.transform()
        self.load()

    def extract(self):
        # You must get the id of Richards with a GET request to /api/merchants endpoint
        self._richards = Merchant(api_request=self._api).search("Richard's")
        if not self._richards:
            raise Exception('Merchant not found')

        self._products = Product(file_path=self._config.products_path, api_request=self._api, merchant_id=self._richards.id)
        self._price_stock = PriceStock(file_path=self._config.price_stock_path, api_request=self._api)


    def transform(self):
        product_transforms = Transforms([
            # The SKU must be unique within the store.
            SkuUnique(),
            # All texts must be cleaned before inserting them into the database. For example, some product
            # descriptions in the files may contain HTML tags, they must be removed.
            TextClean(),
            # Categories and sub-categories in the file must be joined together into a single value containing all
            # categories in lower case and separated by a pipe symbol (|).
            CategoriesJoin(),
            # Some products might have the package information in the description column. Extract the package and store
            # it in its corresponding field in the API.
            PackageExtract(),
        ])
        self._products.set_transforms(product_transforms).transform()

        price_stock_transforms = Transforms([
            # We only want products that are currently in stock, this means their stock is greater than 0.
            StockPositive(),
            # We're only gonna work with branches identified as  `MM` and `RHSM` so we don't need (and don't want) other
            # branches' information in the API.
            BranchFilter(self._config)
        ])
        self._price_stock.set_transforms(price_stock_transforms).transform()

    def load(self):
        # products_df = self._products.get_data()
        # price_stock_df = self._price_stock.get_data()
        # price_stock_df = price_stock_df[~price_stock_df.index.duplicated(keep='first')]
        # merge_df = pd.concat([products_df, price_stock_df], axis=1)
        # # products_df.update(price_stock_df)
        # # print(merge_df)
        # # exit(1)
        # stocks = merge_df[merge_df.index == 302938].to_dict('records')
        # branch_products = [{
        #     'branch': stock['BRANCH'],
        #     'stock': stock['STOCK'],
        #     'price': stock['PRICE'],
        # } for stock in stocks]
        #
        # print(branch_products)

        # Once you have Richard's id then issue a PUT request to /api/merchants/<id> updating the is_active field to
        # True
        if self._richards and self._richards.can_be_updated and not self._richards.is_active:
            self._richards.update(is_active=True)

        # You must delete the store with the name Beauty by issuing a DELETE request to api/ merchants/<id>
        beauty = Merchant(api_request=self._api).search("Beauty")
        if beauty and beauty.can_be_deleted:
            beauty.remove()
        # print(self._richards.name, beauty.name)

        self._products.load({})
