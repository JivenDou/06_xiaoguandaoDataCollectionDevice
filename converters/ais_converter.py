#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2022/11/10
@desc: ais数据解析器
"""

from converter import Converter
from event_storage import EventStorage
from logging_config import shucai_converter as logger


class AisConverter(Converter):

    def __init__(self, name):
        self.__storager = EventStorage()
        self._name = name

    def convert(self, name, data):
        table_name = "table_" + name
        try:
            for info in data:
                # 存实时数据
                sql = f"INSERT IGNORE INTO {table_name} (times, mmsi) VALUES ('{info['times']}', '{info['mmsi']}')"
                self.__storager.execute_sql(sql)
                sql = f"UPDATE {table_name} SET shipname='{info['shipname']}', lon={info['lon']}, " \
                      f"lat={info['lat']}, speed={info['speed']}, course={info['course']}, heading={info['heading']}, " \
                      f"status='{info['status']}', callsign='{info['callsign']}', destination='{info['destination']}', " \
                      f"shiptype='{info['shiptype']}', distance={info['distance']} " \
                      f"WHERE mmsi = '{info['mmsi']}'"
                sql = sql.replace("'None'", "NULL").replace("None", "NULL")
                self.__storager.execute_sql(sql)
                # 存历史数据
                sql = f"INSERT INTO ais_data_history (times, mmsi, lon, lat, speed, course, heading) " \
                      f"VALUES ('{info['times']}', '{info['mmsi']}', {info['lon']}, {info['lat']}, {info['speed']}, {info['course']}, {info['heading']})"
                sql = sql.replace("'None'", "NULL").replace("None", "NULL")
                self.__storager.execute_sql(sql)
        except Exception as e:
            logger.error(repr(e))
