# -*- coding: utf-8 -*-

from integrations.transforms.transform import Transform


class BranchFilter(Transform):

    def execute(self, data):
        return data[data['BRANCH'].isin(self._config.get_allowed_branchs())]
