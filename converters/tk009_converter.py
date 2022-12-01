#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2022/11/06
@desc: GPS数据解析器
"""

from converter import Converter
from event_storage import EventStorage
from logging_config import tk009_converter as logger
import time
import datetime
from datetime import timedelta


class Tk009Converter(Converter):
    def __init__(self, name):
        self.__storager = EventStorage()
        self._name = name

    def convert(self, __save_frequency, data):
        table_name = "xiaoguandao_" + self._name + "_tbl"
        times = datetime.datetime.now()
        times = times.strftime('%Y-%m-%d %H:%M:%S')
        struct_time = time.strptime(times, '%Y-%m-%d %H:%M:%S')
        now_time = time.mktime(struct_time)
        now_time = int(now_time) - int(now_time) % __save_frequency
        save_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now_time))
        try:
            sql = f"INSERT INTO {table_name} (times, lon, lat) " \
                  f"VALUES ('{save_time}', {data['jingdu']}, {data['weidu']})"
            # print(sql)
            self.__storager.execute_sql(sql)
        except Exception as e:
            logger.error(repr(e))
