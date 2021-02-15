# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class ColumnExtract(Transform):
    _column_from: str
    _column_to: str
    _re: str

    def __init__(self, column_from, re, column_to=None, *args, **kwargs):
        super(ColumnExtract, self).__init__(*args, **kwargs)

        self._column_from = column_from
        if not column_to:
            column_to = column_from
        self._column_to = column_to
        self._re = re

    def execute(self, data):
        data[self._column_to] = data[self._column_from].str.extract(self._re)
        return data
