# -*- coding: utf-8 -*-
from collections import Iterator

from integrations.libs.config_source import ConfigSource


class Transform(object):
    _config: ConfigSource

    def __init__(self, config=None):
        if config:
            self._config = config

    def execute(self, data):
        return data


class Transforms(object):
    _transforms: []

    def __init__(self, transforms=list()):
        all = list()
        if isinstance(transforms, list):
            all = transforms

        self._transforms = all

    def __add__(self, transform: Transform):
        self._transforms += transform

    def execute(self, data):
        for transform in self._transforms:
            data = transform.execute(data)
        return data
