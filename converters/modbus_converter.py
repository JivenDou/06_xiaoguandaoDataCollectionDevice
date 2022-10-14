"""
@File  : moxa1_converter.py
@Author: lee
@Date  : 2022/7/12/0012 8:55:13
@Desc  :
"""
import binascii
import math
import struct
from logging_config import shuizhi_file_logger as logger
from converter import Converter
from event_storage import EventStorage


class ModbusConverter(Converter):
    list = []

    def __init__(self):
        self._storage = EventStorage()

    def convert(self, config, data):
        if data:
            device_id = data[0]
            data = data[1]
            # print(device_name, data)
            format_data_dict = {}  # 列表数据转换字典数字
            try:
                for index in config:
                    # addr_type : 'D' 或 'X';
                    # addr_list: [10] 或 [10, 5]
                    addr_type, addr_list = addr_parsing(index['address'])
                    register_addr = addr_list[0]  # 数据地址  example:'X10.5' -> 10
                    parameter_id = addr_list[1]
                    if register_addr > 40000:
                        register_addr = register_addr - 40001
                    if int(index["device_id"]) == int(device_id) and register_addr in data and data[register_addr + 4] == parameter_id:
                        logger.info(f"----------------------------")
                        if addr_type == 'X':
                            bit_offset_addr = addr_list[1]  # 位偏移地址  example:'X10.5' -> 5
                            if index['data_type'] == "BOOL":
                                data_bin = bin(65536 | data[register_addr])  # 和65536做或运算，为了留开头0
                                data_bin = list(data_bin[3:][::-1])  # 去除开头字符 0  b  1并反转字符串
                                data_bin = list(map(int, data_bin))  # 字符列表转整型列表
                                if index['modbus_mode'] == "BA":
                                    data_bin = data_bin[8:16] + data_bin[0:8]
                                if index['negation'] == 1:
                                    return_data = int(bool(1 - data_bin[bit_offset_addr]))  # 取反运算
                                else:
                                    return_data = data_bin[bit_offset_addr]

                        elif addr_type == 'D':
                            if index['data_type'] == "FLOAT16":
                                return_data = data[register_addr]
                            elif index['data_type'] == "INT16":
                                if index['negation'] == 1:
                                    return_data = int(bool(1 - data[register_addr]))  # 取反运算
                                else:
                                    if data[register_addr] > 32767:
                                        return_data = data[register_addr] - 65536
                                    else:
                                        return_data = data[register_addr]
                            elif index['data_type'] == "INT32":
                                return_data_H = data[register_addr]
                                return_data_L = data[register_addr + 1]
                                if index['modbus_mode'] == "CDAB":
                                    return_data = data[register_addr] * 65536 + data[register_addr + 1]
                                else:
                                    return_data = data[register_addr + 1] * 65536 + data[register_addr]
                            elif index['data_type'] == "FLOAT32":
                                t1 = hex(data[register_addr])[2:]
                                t2 = hex(data[register_addr + 1])[2:]
                                if len(t1) < 4:
                                    t1 = (4 - len(t1)) * "0" + t1
                                if len(t2) < 4:
                                    t2 = (4 - len(t2)) * "0" + t2
                                if index['modbus_mode'] == "CDAB":
                                    return_data = \
                                        struct.unpack('>f', binascii.unhexlify((t2 + t1).replace(' ', '')))[0]
                                else:
                                    return_data = \
                                        struct.unpack('>f', binascii.unhexlify((t1 + t2).replace(' ', '')))[0]
                            elif index['data_type'] == "BELZ_FLOAT32":
                                llj_data = []
                                for x in range(0, 6, 2):
                                    t1 = hex(data[register_addr + x])[2:]
                                    t2 = hex(data[register_addr + x + 1])[2:]
                                    if len(t1) < 4:
                                        t1 = (4 - len(t1)) * "0" + t1
                                    if len(t2) < 4:
                                        t2 = (4 - len(t2)) * "0" + t2
                                    t = struct.unpack('>f', binascii.unhexlify((t1 + t2).replace(' ', '')))[0]
                                    llj_data.append(t)
                                return_data = llj_data[0] * 10 ** 6 + llj_data[1] + llj_data[2] / 10 ** 6  # 总累计量
                            elif index['data_type'] == "UINT16":
                                return_data = data[register_addr]
                        logger.info(f"{index['io_point_name']}(格式化前): {return_data}")
                        return_data = format_value(index, return_data)
                        name = 'c' + str(index['serial_number'])
                        format_data_dict[name] = return_data
                        logger.info(f"{index['io_point_name']}: {return_data}")
                return format_data_dict
            except Exception as e:
                logger.error(e)
                return "error"


def addr_parsing(addr_smash):
    """
    :param addr_smash: [X15.1] or [D15]
    :return: X, [15, 1] or D [15]
    """
    # addr_smash_1 = 'D2'
    # addr_smash = list(addr_smash)  # 拆分字符串为list ['X', '6', '.', '2']
    addr_type = addr_smash[0]  # 地址类型 : 'D' 或 'X'
    addr_smash = addr_smash[1:]  # 地址部分: '10' 或 '10.5'
    addr_list = list(map(int, addr_smash.split(".")))  # 用“.”分割字符串转换为整型存入列表
    return addr_type, addr_list


def format_value(index, value):
    if value:
        value = float(value)
        divisor = index['divisor']
        offset = index['offset']
        low_limit = index['low_limit']
        up_limit = index['up_limit']
        if divisor:
            value /= divisor
        if offset:
            value -= offset
        value = round(value, 2)
        if low_limit <= value <= up_limit:
            return value
        else:
            return ''
    else:
        return ''
