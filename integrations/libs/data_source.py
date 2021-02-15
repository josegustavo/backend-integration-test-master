# -*- coding: utf-8 -*-

from pandas.core.frame import DataFrame
from integrations.transforms.transform import Transforms


class DataSource(object):
    _df: DataFrame = None
    _transforms: Transforms = None

    def __init__(self, transforms: Transforms = None, **kwargs):
        if transforms:
            self._transforms = transforms

    def set_transforms(self, transforms: Transforms):
        self._transforms = transforms
        return self

    def get_data(self):
        return self._df

    def transform(self):
        if self._transforms:
            self._df = self._transforms.execute(self._df)
        return self
