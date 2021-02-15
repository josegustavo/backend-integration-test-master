# -*- coding: utf-8 -*-
from integrations.libs.api import Api
from integrations.libs.config_source import ConfigSource
from integrations.models.merchant import Merchant
from integrations.models.price_stock import PriceStock
from integrations.models.product import Product
from integrations.tools.tools import Tools
from integrations.transforms.branch_filter import BranchFilter
from integrations.transforms.column_concat import ColumnConcat
from integrations.transforms.column_rename import ColumnRename
from integrations.transforms.column_extract import ColumnExtract
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
    _products_to_upload = None

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

        self._products = Product(file_path=self._config.products_path, api_request=self._api,
                                 merchant_id=self._richards.id)
        self._price_stock = PriceStock(file_path=self._config.price_stock_path, api_request=self._api)

    def transform(self):
        # Apply filter to products and price stock
        self._products.transform(Transforms([
            # The SKU must be unique within the store.
            SkuUnique(),
        ]))
        allowed_branches = self._config.get_allowed_branches()
        self._price_stock.transform(Transforms([
            # We only want products that are currently in stock, this means their stock is greater than 0.
            StockPositive(),
            # We're only gonna work with branches identified as  `MM` and `RHSM` so we don't need (and don't want) other
            # branches' information in the API.
            BranchFilter(allowed_branches)
        ]))

        # Work with some products
        self._products_to_upload = self._price_stock.merge_products(self._products, allowed_branches)

        # Set merchant ID to all rows
        # endpoint is only allowed to receive products for the merchant_id related to Richard's
        self._products_to_upload['MERCHANT_ID'] = self._richards.id

        # Apply constraints
        self._products_to_upload = Transforms([
            # All texts must be cleaned before inserting them into the database. For example, some product
            # descriptions in the files may contain HTML tags, they must be removed.
            TextClean(columns=['ITEM_DESCRIPTION'], remove_tags=True, is_capitalize=True),
            TextClean(columns=['ITEM_NAME'], is_title=True),

            # Categories and sub-categories in the file must be joined together into a single value containing all
            # categories in lower case and separated by a pipe symbol (|).
            TextClean(columns=['CATEGORY', 'SUB_CATEGORY', 'SUB_SUB_CATEGORY'], is_title=True),
            ColumnConcat(columns=['CATEGORY', 'SUB_CATEGORY', 'SUB_SUB_CATEGORY'], dest='CATEGORY', sep='|'),

            # Some products might have the package information in the description column. Extract the package and store
            # it in its corresponding field in the API.
            ColumnExtract(column_from='ITEM_DESCRIPTION', column_to='PACKAGE',
                          re=r'(\d+\s*(?:un|gr?|kg|ml|lt|cc|pza))'),

            # data stored must meet the data types and semantics of the API structure. i.e: there must be a brand in the
            # Brand field and a URL in the Image URL field, etc.
            ColumnRename(columns={
                'ITEM_DESCRIPTION': 'DESCRIPTION',
                'ITEM_NAME': 'NAME',
                'ITEM_IMG': 'IMAGE_URL',
                'BRAND_NAME': 'BRAND',
            }),
        ]).execute(self._products_to_upload)

    def load(self):

        # Once you have Richard's id then issue a PUT request to /api/merchants/<id> updating the is_active field to
        # True
        if self._richards and self._richards.can_be_updated and not self._richards.is_active:
            self._richards.update(is_active=True)

        # You must delete the store with the name Beauty by issuing a DELETE request to api/ merchants/<id>
        beauty = Merchant(api_request=self._api).search("Beauty")
        if beauty and beauty.can_be_deleted:
            beauty.remove()

        # Once all the filters required with the shared files have been completed, you must send the catalog
        # information to the API
        product_skus = set(self._products_to_upload.index)

        # Prepare data to upload
        for sku in product_skus:
            stocks = self._products_to_upload[self._products_to_upload.index == sku].to_dict('records')
            data = Tools.resume_branch_products(stocks, sku)
            self._api.post_data('/api/products', data)
