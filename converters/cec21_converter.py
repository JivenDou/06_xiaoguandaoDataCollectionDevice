"""
@File  : cec21_converter.py
@Author: lee
@Date  : 2022/8/30/0030 14:42:02
@Desc  : CEC21国产单点流速仪解析器
"""
from logging_config import cec21_converter as logger
from converter import Converter
from tools.format_value import format_value


class CEC21Converter(Converter):
    def __init__(self, name):
        self._name = name

    def convert(self, config, data):
        # 原始data: {'data': b'\x11\x11pval,22.650,-37.896,3.613,11.104,14.158,17.992,70.457,243.563,-8.010,-16.111,11.813,0\r\n'}
        # 格式化数据：['\x11\x11pval', '22.658', '-36.617', '11.304', '10.291', '14.330', '17.643', '82.970', '253.655', '-4.965', '-16.930', '11.813', '0\r\n']
        #                               温度，     pitch，    roll，    X流速，   Y流速，   流速，     方位，   流向，  南 - 北向流速，东 - 西向流速，电压，状态
        try:
            logger.info(f"[{self._name}]原始接收数据: len: {len(data)}, values: {data}")
            data = data.decode('utf-8').split(',')
            logger.info(f"[{self._name}]decode后数据: len: {len(data)}, values: {data}")
            dict = {}
            for index in config:
                name = 'c' + str(index['serial_number'])
                i = int(index['address'])
                dict[name] = format_value(index, data[i])
            logger.info(f"[{self._name}]返回数据: len: {len(dict)}, values: {dict}")
            return dict
        except Exception as e:
            logger.info(f"[{self._name}]：{repr(e)}")
            return
