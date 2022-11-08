#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2021/5/31 11:37
@desc: 水质、水文、太阳能的解析器
"""

from converter import Converter
from logging_config import shucai_converter as logger


class ShucaiConverter(Converter):

    # def __init__(self):
    #

    def convert(self, config, data):
        if data:
            try:
                format_data_dict = {}
                for index in config:
                    name = 'c' + str(index['serial_number'])
                    if data[index['address']] is not None:
                        format_data_dict[name] = data[index['address']]
                return format_data_dict
            except Exception as e:
                logger.error(e)
                return "error"
