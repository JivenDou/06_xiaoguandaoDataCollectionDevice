#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2022/11/06
@desc: 水质、水文、太阳能数据解析器
"""

from converter import Converter
from event_storage import EventStorage
from logging_config import shucai_converter as logger


class ShucaiConverter(Converter):
    def __init__(self, name):
        self.__storager = EventStorage()
        self._name = name

    def convert(self, name, data):
        table_name = "table_" + name
        try:
            k_list = [key for key in data.keys()]
            v_list = [str(data[key]) for key in data.keys()]
            sql = f"INSERT INTO {table_name} ({','.join(k_list)}) VALUE ({','.join(v_list)})"
            self.__storager.execute_sql(sql)
        except Exception as e:
            logger.error(repr(e))
