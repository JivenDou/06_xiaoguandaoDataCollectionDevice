"""
@File  : dandian_converter.py
@Author: lee
@Date  : 2022/8/30/0030 14:42:02
@Desc  :
"""
import json
import re
from logging_config import dandian_file_logger as logger
from converter import Converter


class DandianConverter(Converter):
    def convert(self, config, data):
        # 原始data: {'data': b'\x11\x11pval,22.650,-37.896,3.613,11.104,14.158,17.992,70.457,243.563,-8.010,-16.111,11.813,0\r\n'}
        # 格式化数据：['\x11\x11pval', '22.658', '-36.617', '11.304', '10.291', '14.330', '17.643', '82.970', '253.655', '-4.965', '-16.930', '11.813', '0\r\n']
        #                               温度，     pitch，    roll，    X流速，   Y流速，   流速，     方位，   流向，  南 - 北向流速，东 - 西向流速，电压，状态
        try:
            data = data.decode('utf-8').split(',')
            logger.info(f"(新版单点流速仪)原始数据: {data}")
            dict = {}
            for index in config:
                name = 'c' + str(index['serial_number'])
                i = int(index['address'])
                if index['divisor'] is None:
                    dict[name] = float(data[i])
                else:
                    dict[name] = round((float(data[i]) / index['divisor']), 2)
            logger.info(f"(新版单点流速仪)解析后数据：{data}")
            return dict
        except Exception as e:
            logger.error(e)
            return "error"
