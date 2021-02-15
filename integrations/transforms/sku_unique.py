# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class SkuUnique(Transform):

    def execute(self, data):
        data = data.loc[~data.index.duplicated(keep='first')]
        # data = data[~data.index.duplicated(keep='first')]
        return data