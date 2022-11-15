#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2021/5/31 11:37
@desc: http连接器
"""
import datetime
import json
import queue
import time
import traceback
import threading
import requests
from connector import Connector
from event_storage import EventStorage
from logging_config import ais_http_connector as logger


class ShuCaiHttpConnector(Connector, threading.Thread):
    __master = 0
    _disConnectTime = 0

    def __init__(self, name, config, converter):
        super().__init__()
        self.__master = None
        self.__stopped = False
        self.__connected = False
        self.__save_frequency = config['save_frequency']  # 数据存储时间间隔
        self.setDaemon(True)
        self.setName(name)
        self.__converter = converter
        self.__storager = EventStorage()
        self.__command_queue = queue.Queue(50)
        self.__last_save_time = 0
        self.__data_point_config = self.__storager.get_station_info(name)
        self.__url = config['url']
        self.__before_seconds = config['before_seconds']
        self._name = name

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connected = True
        while True:
            time.sleep(self.__before_seconds)
            now_time = datetime.datetime.now()
            before_time = now_time - datetime.timedelta(seconds=self.__before_seconds)
            post_data = {
                "timeBegin": before_time.strftime("%H:%M:%S"),
                "timeEnd": now_time.strftime("%H:%M:%S")
            }
            # print(post_data)
            data = []
            try:
                result = requests.post(self.__url, json=post_data, timeout=0.5)
                data = json.loads(result.text)
            except Exception as e:
                logger.error(f'shucai http connect error:{repr(e)}')
                time.sleep(5)
            # 数据传入解析器
            if data:
                logger.info(f"data_len : {len(data)}")
                self.__converter.convert(self._name, data)
            else:
                logger.info("data is None")

    def __connect(self):
        pass

    def __reconnect(self):
        pass

    def close(self):
        pass

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.__connected

    def send_command(self, content):
        pass

    def command_polling(self, result, resend_times=None):
        format_data = None
        if result:
            format_data = self.__converter.convert(self.__data_point_config, result)
        if format_data:
            if format_data != "error" and format_data != 'pass':
                # 往redis存储数据
                self.__storager.real_time_data_storage(format_data)
