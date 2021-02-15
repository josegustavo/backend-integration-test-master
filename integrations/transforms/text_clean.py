# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class TextClean(Transform):
    _columns: list = []
    _is_title = False
    _is_capitalize = False
    _remove_tags=False

    def __init__(self, columns: list = [], remove_tags=False, is_title=False, is_capitalize = False, *args, **kwargs):
        super(TextClean, self).__init__(*args, **kwargs)

        self._columns = columns
        self._remove_tags = remove_tags
        self._is_title = is_title
        self._is_capitalize = is_capitalize

    def execute(self, data):
        for column in self._columns:
            if self._remove_tags:
                data[column] = data[column].str.replace('<[^<]+?>', '')

            if self._is_capitalize:
                data[column] = data[column].str.capitalize()

            elif self._is_title:
                data[column] = data[column].str.title()

        return data
