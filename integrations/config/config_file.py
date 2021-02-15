# -*- coding: utf-8 -*-
from configparser import ConfigParser
from integrations.libs.config_source import ConfigSource


class ConfigFile(ConfigSource):

    def __init__(self):
        super(ConfigFile, self).__init__()
