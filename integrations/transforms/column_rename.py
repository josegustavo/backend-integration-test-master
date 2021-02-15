# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class ColumnRename(Transform):
    _columns: dict = {}

    def __init__(self, columns=None, *args, **kwargs):
        super(ColumnRename, self).__init__(*args, **kwargs)

        if columns is None:
            columns = {}
        self._columns = columns

    def execute(self, data):
        if self._columns:
            data.rename(columns=self._columns, inplace=True)
        return data
