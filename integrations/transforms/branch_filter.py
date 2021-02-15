# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class BranchFilter(Transform):

    _allowed_branches = []

    def __init__(self, allowed_branches = [], *args, **kwargs):
        super(BranchFilter, self).__init__(*args, **kwargs)

        self._allowed_branches = allowed_branches

    def execute(self, data):
        if self._allowed_branches:
            data = data[data['BRANCH'].isin(self._allowed_branches)]
        return data
