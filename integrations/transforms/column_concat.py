# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class ColumnConcat(Transform):
    _columns: list = []
    _dest: str
    _sep: str

    def __init__(self, columns, dest, sep='›', *args, **kwargs):
        super(ColumnConcat, self).__init__(*args, **kwargs)

        self._columns = columns
        self._dest = dest
        self._sep = sep

    def execute(self, data):
        if self._dest:
            for col in self._columns:
                data[col] = data[col].map(str)
            data[self._dest] = data[self._columns].agg(self._sep.join, axis=1)
            for col in self._columns:
                if col != self._dest:
                    del data[col]

        return data
