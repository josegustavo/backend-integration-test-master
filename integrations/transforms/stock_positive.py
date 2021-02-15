# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class StockPositive(Transform):

    def execute(self, data):
        return data[data['STOCK'] > 0]
