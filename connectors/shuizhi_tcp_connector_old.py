"""
@Date  :2021/5/21/00219:10:57
@Desc  :
"""
import binascii
import threading
import time
import struct
import socket
from connector import Connector
from event_storage import EventStorage
from log import Log

sendFlag = 0


class ShuizhiTcpConnector(Connector, threading.Thread):
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
        self.setName(name)
        self.__last_seve_time = 0
        self.__data_point_config = self.__storager.get_station_info(name)
        # for i in self.__data_point_config:
        #     print(i)

    def open(self):
        self.__stopped = False
        self.start()

    # 建立socket连接
    def __connect(self):
        if self.__sock:
            self.close()
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
        try:
            self.__sock.connect((self.__ip, self.__port))
            self.__log.info(f'Connect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] success !')
            self.__connected = True
        except socket.error as e:
            self.__log.info(f'Connect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] failed:{e} !!!')
            self.__connected = False
            self.__reconnect()

    def __reconnect(self):
        while True:
            try:
                self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.__sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)  # 在客户端开启心跳维护
                self.__sock.connect((self.__ip, self.__port))
                self.__connected = True
                self.__log.info(f'Reconnect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] success !')
                break
            except Exception as e:
                print("Continue reconnect in 5s..")
                self.__log.info(
                    f'Reconnect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] failed:{e} !!! Continue reconnect in 5s..')
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

    def send_command(self, command_list):
        pass

    def command_polling(self):
        pass

    def run(self):
        self.__connect()
        self.__connected = True
        # dissolved_oxygen = bytes.fromhex('01030025000AD406')  # 读溶解氧发送指令，接收数据长度：25
        dissolved_oxygen = bytes.fromhex('010315CF0005B1FA')  # 读溶解氧发送指令，接收数据长度：15
        temperature_salinity = bytes.fromhex('010300FF001AF431')  # 读温度和盐度发送指令，接收数据长度：52 + 5 = 57
        PH = bytes.fromhex('010301D90002140C')  # 读PH发送指令，数据接收长度：4 + 5 = 9
        # chlorophyll = bytes.fromhex('010316A1000411A3')  # 读叶绿素发送指令，接收数据长度：8 + 5 = 13
        chlorophyll = bytes.fromhex('010316A80004C1A1')  # 读叶绿素发送指令，接收数据长度：8 + 5 = 13

        # depth = bytes.fromhex('0103046F0012F4EA')  # 读深度发送指令，接收数据长度：36 + 5 = 41
        # depth = bytes.fromhex('0103155100035016')  # 读深度发送指令，接收数据长度：6 + 5 = 11
        depth = bytes.fromhex('010315660003E1D8')  # 读深度发送指令，接收数据长度：6 + 5 = 11
        # 01 03 06 40 BA FD 82 00 00 67 EA 返回数据测试

        # 创建接收线程
        threading.Thread(target=self.SocketReceive, args=(self.__sock,)).start()

        while 1:
            time.sleep(0.2)
            if not self.__connected:
                continue
            try:
                if sendFlag == 0:
                    self.__sock.send(depth)
                elif sendFlag == 1:
                    self.__sock.send(dissolved_oxygen)
                elif sendFlag == 2:
                    self.__sock.send(depth)
                elif sendFlag == 3:
                    self.__sock.send(temperature_salinity)
                elif sendFlag == 4:
                    self.__sock.send(depth)
                elif sendFlag == 5:
                    self.__sock.send(PH)
                elif sendFlag == 6:
                    self.__sock.send(depth)
                elif sendFlag == 7:
                    self.__sock.send(chlorophyll)
                elif sendFlag == 8:
                    self.__sock.send(depth)
            except Exception as e:
                self.__connected = False
                self.__reconnect()
                threading.Thread(target=self.SocketReceive, args=(self.__sock,)).start()
            if self.__stopped:
                break

    # 水质解析器
    def save_format_data(self, t, name):
        data = {}
        for index in self.__data_point_config:
            if index["io_point_name"] == name:
                if index['divisor'] is not None:
                    t = t / index['divisor']
                if index['offset'] is not None:
                    t = t - index['offset']
                if index['low_limit'] is not None and index['up_limit'] is not None and index['low_limit'] <= t <= \
                        index['up_limit']:
                    data = {'c' + str(index['serial_number']): t}
                    self.__storager.real_time_data_storage(data)
        print(data)

    def SocketReceive(self, clientSocket):
        global sendFlag
        ''' Socket 接收线程。'''
        # global socket_flag, socket_msg  # 通过全局变量，让外部可以控制线程的运行，也可以处理信息

        while 1:
            time.sleep(0.5)
            # print(sendFlag, time.time())
            # 深度
            if sendFlag == 0:
                try:
                    # print(clientSocket)
                    recvData = clientSocket.recv(1024)
                except Exception as e:
                    # print("深度1", e)
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 11:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('----深度:', t, 'res:', len(res), 'length:', length, time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "深度")
                    sendFlag = 1
            # 溶解氧
            if sendFlag == 1:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                # print(time.strftime('%Y-%m-%d %H:%M:%S'))
                if length == 15:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('溶解氧:', t, 'res:', len(res), 'length:', length, time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "溶解氧")
                    sendFlag = 2
            # 深度
            if sendFlag == 2:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 11:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('深度:', t, 'length:', length, time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "深度")
                    sendFlag = 3
            # 温度、盐度
            if sendFlag == 3:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 57:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('温度:', t, 'len:', len(res), time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "温度")

                    q = int_to_hex(res[-6], res[-5], res[-4], res[-3])
                    print('盐度:', q, 'len:', len(res), time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(q, "盐度")
                    sendFlag = 4
            # 深度
            if sendFlag == 4:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 11:
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('深度:', t, 'length:', length, time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "深度")
                    sendFlag = 5
            # PH
            if sendFlag == 5:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 9:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    # print('PH:', t, 'len:', len(res), time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "PH")
                    sendFlag = 6
            # 深度
            if sendFlag == 6:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 11:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('深度:', t, 'length:', length, time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "深度")

                    sendFlag = 7
            # 叶绿素
            if sendFlag == 7:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 13:
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    # print('叶绿素:', t, 'len:', len(res), time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "叶绿素")
                    sendFlag = 8
            # 深度
            if sendFlag == 8:
                try:
                    recvData = clientSocket.recv(1024)
                except Exception as e:  # 忽视掉超时
                    break
                length = len(recvData)
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                if length == 11:
                    # print(len(res), res)
                    t = int_to_hex(res[3], res[4], res[5], res[6])
                    print('深度:', t, 'len:', len(res), time.strftime('%Y-%m-%d %H:%M:%S'))
                    self.save_format_data(t, "深度")
                    sendFlag = 0
        clientSocket.close()
        self.__log.info("Client closed.")

        # print(time.strftime('%Y-%m-%d %H:%M:%S'), len(recvData))
        # socket_msg = recvData.decode()  # 将接收到的字节数据转为 string
        # print("Socket receive: " + socket_msg)


def int_to_hex(a1, a2, b1, b2):
    t1 = hex(a1 * 256 + a2)[2:]
    t2 = hex(b1 * 256 + b2)[2:]
    if len(t1) != 4: t1 = (4 - len(t1)) * '0' + t1
    if len(t2) != 4: t2 = (4 - len(t2)) * '0' + t2
    t = t1 + t2
    t = struct.unpack('>f', binascii.unhexlify(t.replace(' ', '')))[0]
    return t
