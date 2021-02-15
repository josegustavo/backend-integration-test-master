# -*- coding: utf-8 -*-
import pandas as pd
from pandas._typing import FilePathOrBuffer

from integrations.libs.api import Api
from integrations.libs.data_source import DataSource


class DataCsv(DataSource):
    __sep = '|'
    _file_path: str
    _columns: list
    _index = []

    def __init__(self, file_path: FilePathOrBuffer = None, api_request: Api = None, *args, **kwargs):
        super(DataCsv, self).__init__(*args, **kwargs)

        if api_request:
            self._api = api_request

        if file_path:
            self._file_path = file_path
            self.download_data()

    def download_data(self):
        self._df = pd.read_csv(self._file_path, sep=self.__sep, usecols=self._columns, index_col=self._index)