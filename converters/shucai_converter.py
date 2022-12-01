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

    def convert(self, config, data):
        try:
            for d in data:
                if data[d] is None or data[d] == '':
                    data[d] = ''
                else:
                    data[d] = float(data[d])
            return data
        except Exception as e:
            logger.error(repr(e))
