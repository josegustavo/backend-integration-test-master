# -*- coding: utf-8 -*-

from integrations.data_input.data_csv import DataCsv
from integrations.models.product import Product
from integrations.transforms.sku_unique import SkuUnique


class PriceStock(DataCsv):
    _columns = ['SKU', 'BRANCH', 'PRICE', 'STOCK']

    _index = 'SKU'

    # Merge Data of Products and Price Sotock and return the Products to upload
    def merge_products(self, products: Product, allowed_branches: list, qty_branch=100):
        products_df = products.get_data()
        price_stock_df = self.get_data()

        stock_products_df = price_stock_df.merge(products_df, left_index=True, right_index=True)
        stock_products_df = stock_products_df.sort_values(by=['BRANCH', 'PRICE'], ascending=False)
        stock_products_unique_df = SkuUnique().execute(stock_products_df)

        product_skus = []
        # Select the most expensive products of each branch
        for branch in allowed_branches:
            most_expensive_df = stock_products_unique_df[stock_products_unique_df['BRANCH'] == branch].head(qty_branch)
            product_skus += most_expensive_df.index.to_list()
        product_skus = list(set(product_skus))

        products_to_upload = stock_products_df[stock_products_df.index.isin(product_skus)]
        return products_to_upload
