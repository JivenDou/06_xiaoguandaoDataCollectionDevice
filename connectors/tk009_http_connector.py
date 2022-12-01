#!/usr/bin/env python
# encoding: utf-8
"""
@time: 2021/5/31 11:37
@desc: http连接器
"""
import json
import queue
import time
import threading
import requests
from connector import Connector
from event_storage import EventStorage
from logging_config import tk009_http_connector as logger


class Tk009HttpConnector(Connector, threading.Thread):
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
        self.__login_name = "Sencott"
        self.__login_password = "123456"
        self.__mds = None
        self.__object_id = None

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connected = True
        while True:
            try:
                # 登录
                url = f"{self.__url}/GetDateServices.asmx/loginSystem?" \
                      f"LoginName={self.__login_name}&LoginPassword={self.__login_password}&" \
                      f"LoginType=ENTERPRISE&language=cn&ISMD5=0&timeZone=+08&apply=APP"
                result = requests.post(url, timeout=1)
                data = json.loads(result.text)
                if data['success'] == 'true':
                    self.__mds = data['mds']
                # 获取 object id
                url = f"{self.__url}/GetDateServices.asmx/GetDate?method=getDeviceList&mds={self.__mds}"
                result = requests.post(url, timeout=1)
                data = json.loads(result.text)
                if data['success'] == 'true':
                    self.__object_id = data['rows'][0]['objectid']
                # 获取设备详细信息
                url = f"{self.__url}/GetDateServices.asmx/GetDate?method=loadUser&user_id={self.__object_id}&mds={self.__mds}"
                result = requests.post(url, timeout=1)
                data = json.loads(result.text)
                if data['success'] == 'true':
                    data = data["data"][0]
                # 数据传入解析器
                if data:
                    self.__converter.convert(self.__save_frequency, data)
                else:
                    logger.info(f"{self._name} data is None")
                time.sleep(self.__save_frequency)
            except Exception as e:
                logger.error(f'{self._name} http connect error:{repr(e)}')
                time.sleep(self.__save_frequency)

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
