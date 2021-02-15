# -*- coding: utf-8 -*-

class Tools(object):

    @staticmethod
    def resume_branch_products(stocks:dict, sku:str):
        ignore_columns = ['PRICE', 'STOCK']
        result = {
            'sku': str(sku),
            'barcodes': [],
            'url': '/' + str(sku) + '/',
        }
        for key, value in stocks[0].items():
            if key not in ignore_columns:
                result[key.lower()] = stocks[0][key]

        result['branch_products'] = [{
            'branch': stock['BRANCH'],
            'stock': stock['STOCK'],
            'price': stock['PRICE'],
        } for stock in stocks]

        return result