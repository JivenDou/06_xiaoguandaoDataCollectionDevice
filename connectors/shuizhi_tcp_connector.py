"""
@Date  :2021/5/21/00219:10:57
@Desc  : 原本用于insitu水质传感器的读取和解析，目前此连接器未启动，insitu读取和解析均为mudbus_rtu_over_tcp。
"""
import binascii
import threading
import time
import struct
import socket
from connector import Connector
from event_storage import EventStorage
# from logging_config import shuizhi_converter as logger
from binascii import *
from crcmod import *

sendFlag = 0


class ShuizhiTcpConnector(Connector, threading.Thread):
    def __init__(self, name, config, converter):
        super().__init__()
        self._param_id = {}
        self._len_param = None
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
        self._storage = EventStorage()

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
            logger.info(f'Connect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] success !')
            self.__connected = True
        except socket.error as e:
            logger.error(f'Connect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] failed:{e} !!!')
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
                logger.info(f'Reconnect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] success !')
                break
            except Exception as e:
                logger.info(f'Reconnect to [{self.get_name()}]:[{self.__ip}]:[{self.__port}] failed:{e} !!! Continue reconnect in 5s..')
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
        # dissolved_oxygen = bytes.fromhex('01 03 15 CF 00 05 B1 FA')    # 读溶解氧发送指令，接收数据：
        # temperature = bytes.fromhex('01 03 15 4A 00 05 A0 13')  # 读温度发送指令，接收数据：01 03 0A 41 C0 BC 1C 00 00 00 01 00 01 61 42
        # salinity = bytes.fromhex('01 03 15 97 00 05 30 29')     # 读盐度发送指令，接收数据：01 03 0A 00 00 00 00 00 00 00 61 00 0C 75 6D
        # PH = bytes.fromhex('01 03 15 BA 00 05 A0 20')           # 读 PH 发送指令，接收数据：01 03 0A 40 F9 2B 79 00 00 00 91 00 11 72 BB
        # chlorophyll = bytes.fromhex('01 03 16 A8 00 05 00 61')  # 读叶绿素发送指令，接收数据：01 03 0A 00 00 00 00 00 00 01 01 00 33 34 9F
        # depth = bytes.fromhex('01 03 15 66 00 05 61 DA')        # 读深度发送指令，接收数据：01 03 0A 42 08 1B F4 00 00 00 26 00 05 34 D0

        # 获取需要读取的参数的相关信息
        param_list = self._storage.get_in_situ_command()
        depth_index = None
        depth = ""
        # ①判断参数中是否有 深度, ②处理 寄存器偏移量 的位置
        for each in param_list:
            self._param_id[each["parameter_id"]] = each["name"]
            if each["name"] == "深度":
                crc_check = crc16Add(each['station_code'] + each["function_code"] + dec_to_hex(each["address"]) + "0005")
                depth = bytes.fromhex(crc_check)
                depth_index = param_list.index(each)
        if depth_index is not None:
            param_list.pop(depth_index)
        instruct_list = []
        if len(depth) > 0:
            for each in param_list:
                crc_check = crc16Add(each['station_code'] + each["function_code"] + dec_to_hex(each["address"]) + "0005")
                instruct_list.append(depth)
                instruct_list.append(bytes.fromhex(crc_check))
            instruct_list.append(depth)
        else:
            for each in param_list:
                crc_check = crc16Add(each['station_code'] + each["function_code"] + dec_to_hex(each["address"]) + "0005")
                instruct_list.append(bytes.fromhex(crc_check))
        self._len_param = len(instruct_list)

        # 创建接收线程
        threading.Thread(target=self.SocketReceive, args=(self.__sock,)).start()
        # 循环发送指令
        while 1:
            time.sleep(0.5)
            if not self.__connected:
                continue
            try:
                for i in instruct_list:
                    # self.__sock.send(instruct_list[sendFlag])\
                    time.sleep(1)
                    self.__sock.send(i)
                    time.sleep(1)
                    self.__sock.send(i)
            except Exception as e:
                self.__connected = False
                self.__reconnect()
                threading.Thread(target=self.SocketReceive, args=(self.__sock,)).start()
            if self.__stopped:
                break

    def save_format_data(self, t, name):
        data = {}
        for index in self.__data_point_config:
            if index["io_point_name"] == name:
                if index['divisor'] is not None:
                    t = t / index['divisor']
                if index['offset'] is not None:
                    t = t - index['offset']
                data = {'c' + str(index['serial_number']): t}
                self.__storager.real_time_data_storage(data)

    def SocketReceive(self, clientSocket):
        global sendFlag
        ''' Socket 接收线程。'''
        while 1:
            time.sleep(0.2)
            try:
                recvData = clientSocket.recv(1024)
            except Exception as e:
                logger.info(f"Socket receive error:{e}")
                break
            length = len(recvData)
            if length == 15:
                fmt = str(length) + 'B'
                res = struct.unpack(fmt, recvData)
                t = int_to_hex(res[3], res[4], res[5], res[6])
                logger.info(f" {self._param_id[res[12]]},   t= {t}")
                self.save_format_data(t, self._param_id[res[12]])
            else:
                logger.info(f"读取错误:{recvData}，跳过。")
            # if sendFlag == self._len_param - 1:
            #     logger.info("-------------------")
            #     sendFlag = 0
            # else:
            #     sendFlag = sendFlag + 1
        clientSocket.close()
        logger.info("Client closed.")


def int_to_hex(a1, a2, b1, b2):
    t1 = hex(a1 * 256 + a2)[2:]
    t2 = hex(b1 * 256 + b2)[2:]
    if len(t1) != 4: t1 = (4 - len(t1)) * '0' + t1
    if len(t2) != 4: t2 = (4 - len(t2)) * '0' + t2
    t = t1 + t2
    t = struct.unpack('>f', binascii.unhexlify(t.replace(' ', '')))[0]
    return t


def dec_to_hex(num):
    """
    十进制转十六进制
    """
    t = hex(num)
    t = (6 - len(t)) * "0" + t[2:]
    return t


# CRC16-MODBUS
def crc16Add(read):
    """
    生成CRC16校验位
    """
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc=0xFFFF, xorOut=0x0000)
    data = read.replace(" ", "")
    read_crcout = hex(crc16(unhexlify(data))).upper()
    str_list = list(read_crcout)
    if len(str_list) < 6:
        str_list.insert(2, '0' * (6 - len(str_list)))  # 位数不足补0
    crc_data = "".join(str_list)
    read = read.strip() + '' + crc_data[4:] + '' + crc_data[2:4]
    return read
