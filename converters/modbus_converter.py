"""
@File  : modbus_converter.py
@Author: lee
@Date  : 2022/7/12/0012 8:55:13
@Desc  : 此类为mosbus协议通用解析器，用于：insitu水质传感器，新气象传感器，新水质传感器
"""
import binascii
import math
import struct
from logging_config import modbus_converter as logger
from converter import Converter
from event_storage import EventStorage
from tools.format_value import format_value


class ModbusConverter(Converter):
    def __init__(self, name):
        self._storage = EventStorage()
        self._name = name

    def convert(self, config, data):
        """
        data: [1, {112: 16801, 113: 50856}]
              [站号， {地址：值，地址：值 。。。}]
        """
        if data:
            device_id = data[0]
            data = data[1]
            # print(device_name, data)
            format_data_dict = {}  # 列表数据转换字典数字
            try:
                for index in config:
                    if int(index["device_id"]) == int(device_id):
                        # addr_type : 'D' 或 'X';
                        # addr_list: [10] 或 [10, 5]
                        addr_type, addr_list = addr_parsing(index['address'])
                        register_addr = addr_list[0]  # 数据地址  example:'X10.5' -> 10
                        # parameter_id = addr_list[1]
                        # print(parameter_id)
                        if register_addr > 40000:
                            register_addr = register_addr - 40001
                        # if register_addr in data and data[register_addr + 4] == parameter_id:
                        if register_addr in data:
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
                                        return_data = struct.unpack('>f', binascii.unhexlify((t2 + t1).replace(' ', '')))[0]
                                    elif index['modbus_mode'] == "DCBA":
                                        t1_l, t1_r = t1[0:2], t1[2:4]
                                        t2_l, t2_r = t2[0:2], t2[2:4]
                                        t1, t2 = t1_r + t1_l, t2_r + t2_l
                                        return_data = struct.unpack('>f', binascii.unhexlify((t2 + t1).replace(' ', '')))[0]
                                    else:
                                        return_data = struct.unpack('>f', binascii.unhexlify((t1 + t2).replace(' ', '')))[0]
                                    # 电导率转盐度
                                    if index['io_point_name'] == "盐度" and self._name == 'shuzhi_new':
                                        return_data = self.cal_salty(return_data)

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
                            name = 'c' + str(index['serial_number'])
                            # 格式化数据
                            format_data_dict[name] = format_value(index, return_data)
                            logger.info(f"[{self._name}]: {index['io_point_name']}: {format_data_dict}")
                return format_data_dict
            except Exception as e:
                logger.error(f"{self._name}:{repr(e)}")
                return "error"

    def cal_salty(self, conductivity):
        """盐度转换:需要温度和深度参数"""
        sql = f"SELECT serial_number FROM data_point_tbl WHERE device_name = '{self._name}' AND io_point_name = '温度'"
        sql1 = f"SELECT serial_number FROM data_point_tbl WHERE device_name = '{self._name}' AND io_point_name = '深度'"
        res = self._storage.execute_sql(sql)
        res1 = self._storage.execute_sql(sql1)
        serial_number_temperature = 'c' + str(res[0]['serial_number'])
        serial_number_deep = 'c' + str(res1[0]['serial_number'])
        data = self._storage.get_real_data([serial_number_temperature, serial_number_deep])
        a0, a1, a2, a3, a4, a5 = 0.0080, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081
        b0, b1, b2, b3, b4, b5 = 0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144
        c0, c1, c2, c3, c4 = 0.6766097, 2.00564e-2, 1.104259e-4, -6.9698e-7, 1.0031e-9
        d1, d2, d3, d4 = 3.426e-2, 4.464e-4, 4.215e-1, -3.107e-3
        e1, e2, e3 = 2.070e-5, -6.370e-10, 3.989e-15
        k = 0.0162
        R = conductivity / 42.914

        try:
            if data[serial_number_temperature] and data[serial_number_deep]:
                t = float(data[serial_number_temperature]) * 1.00024
                p = float(data[serial_number_deep])

                rt = c0 + c1 * t + c2 * t * t + c3 * t * t * t + c4 * t * t * t * t
                Rp = 1 + p * (e1 + e2 * p + e3 * p * p) / (1 + d1 * t + d2 * t * t + (d3 + d4 * t) * R)
                Rt = R / (Rp * rt)
                # print("\nRt=",Rt,'\n')
                S = (t - 15) * (b0 + b1 * math.sqrt(Rt) + b2 * Rt + b3 * Rt * math.sqrt(Rt) + b4 * Rt * Rt + b5 * Rt * Rt * math.sqrt(Rt)) / (1 + k * (t - 15))
                Salinity = a0 + a1 * math.sqrt(Rt) + a2 * Rt + a3 * Rt * math.sqrt(Rt) + a4 * Rt * Rt + a5 * Rt * Rt * math.sqrt(Rt) + S
                return Salinity
            else:
                return None
        except Exception as e:
            logger.error(f"{self._name}:{repr(e)}")
            return 0.00


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
