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
from logging_config import http_connector as logger


class HttpConnector(Connector, threading.Thread):
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
        self.__command = self.__storager.get_command_info(name)
        self.__url = config['url']
        self._name = name

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connected = True
        command_list = json.loads(self.__command[0]['command'])
        while True:
            data = []
            for i in range(len(command_list)):
                postdata = command_list['data']
                s = requests.session()
                try:
                    s.keep_alive = False
                    result = requests.post(self.__url, json=postdata, timeout=0.1)
                    data = json.loads(result.text)
                except Exception as e:
                    logger.error(f'{self._name} http connect error:{repr(e)}')
                self.command_polling(data, resend_times=5)
            time.sleep(5)

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
            logger.info(f"format_data:{format_data}")
        else:
            logger.info(f"{self._name} data is None")

        if format_data:
            if format_data != "error" and format_data != 'pass':
                # 往redis存储数据
                self.__storager.real_time_data_storage(format_data)
