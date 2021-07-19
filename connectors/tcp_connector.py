"""
@Date  :2021/5/21/00219:10:57
@Desc  :
"""
import time
import threading
import struct
import socket
import queue
import traceback
from log import Log
from connector import Connector
from event_storage import EventStorage


class TcpConnector(Connector, threading.Thread):
    def __init__(self, name, config, converter):
        super().__init__()
        self.__log = Log()
        self.__sock = None
        self.__connected = False
        self.__stopped = False
        self.__size = 1024
        self.__ip = config['ip']
        self.__port = config['port']
        self.__converter = converter
        self.__storager = EventStorage()
        self.__save_frequency = config['save_frequency']
        self.__command_queue = queue.Queue(50)
        self.setName(name)
        self.__last_seve_time = 0
        self.__data_point_config = self.__storager.get_station_info(name)

    def open(self):
        self.__stopped = False
        self.start()

    def run(self):
        self.__connect()
        self.__connected = True
        while True:
            time.sleep(1)
            self.command_polling()
            if self.__stopped:
                break

    # 建立socket连接
    def __connect(self):
        if self.__sock:
            self.close()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 允许重用本地地址和端口
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
        self.__sock.settimeout(180)  # 设置超时时间3mins
        try:
            self.__sock.connect((self.__ip, self.__port))
            self.__log.info(f'Connect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] success !')
            self.__connected = True
        except Exception as e:
            self.__log.info(f'Connect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] failed:{e} !!!')
            self.__connected = False
            self.__reconnect()

    def __reconnect(self):
        while True:
            try:
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
                self.__sock.settimeout(180)  # 设置超时时间3mins
                self.__sock.connect((self.__ip, self.__port))
                self.__connected = True
                self.__log.info(f'Reconnect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] success !')
                break
            except Exception as e:
                self.__log.info(f'Reconnect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] failed:{e} !!! Continue reconnect in 5s..')
                self.__connected = False
                time.sleep(5)

    def close(self):
        """Close the connection with the TCP Slave"""
        if self.__sock:
            self.__sock.close()
            self.__stopped = True
            self.__sock = None
            self.__connected = False
            return None

    def get_name(self):
        return self.name

    def is_connected(self):
        return self.__connected

    def send_command(self, data):
        if self.__sock:
            try:
                self.__sock.send(data.encode(encoding='utf-8'))
            except Exception as e:
                self.__log.info(f'Send command to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] error:{e}')

    def command_polling(self):
        if self.__connected:
            try:
                time.sleep(0.2)
                data = self.__sock.recv(self.__size)
                data = self.__converter.convert(self.__data_point_config, data)
                print(data)
                if data:
                    if data != "error" and data != 'pass':
                        self.__storager.real_time_data_storage(data)
            except Exception as e:
                self.__log.error(f'Other error occur [{self.get_name()}]:[{self.__ip}]:[{self.__port}]:{e}')
                time.sleep(5)
                self.__reconnect()
        else:
            self.__reconnect()
