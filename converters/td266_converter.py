import json
import re
from sanic.log import logger

from converter import Converter


class TD266Converter(Converter):
    def convert(self, config, data):
        try:
            data = data.decode('utf-8').split('\t')
            logger.info(f"原始数据(单点流速仪): {data}")
            dict = {}
            for index in config:
                name = 'c' + str(index['serial_number'])
                i = int(index['address'])
                if index['divisor'] is None:
                    dict[name] = float(data[i])
                else:
                    dict[name] = round((float(data[i]) / index['divisor']), 2)
            logger.info(f"解析后数据(单点流速仪)：{data}")
            return dict
        except Exception as e:
            logger.error(e)
            return "error"


"""
    def convert(self, config, data):
        # 原始data: data = b'4420\t1194\t29.823\t104.507\t-7.471\t28.872\t253.153\t9.369\t1.816\t91.491\t-59.593\t100\t9.542\t9.589\t0.015\r\n'
        # 去除结尾\r\n: data = b'4420\t1194\t29.823\t104.507\t-7.471\t28.872\t253.153\t9.369\t1.816\t91.491\t-59.593\t100\t9.542\t9.589\t0.015'
        # decode('utf-8'): data = 4420	1194	29.823	104.507	-7.471	28.872	253.153	9.369	1.816	91.491	-59.593	100	9.542	9.589	0.015
        # split('\t'): data = ['4420', '1194', '29.823', '104.507', '-7.471', '28.872', '253.153', '9.369', '1.816', '91.491', '-59.593', '100', '9.542', '9.589', '0.015']
        # logger.debug(len(data), time.strftime('%Y-%m-%d %H:%M:%S'), data)
        pattern_start = b"4420"
        # pattern_end = b"\r\n"
        index_start = re.search(pattern_start, data)  # 查找字符串得到开始索引
        # index_end = re.search(pattern_end, data)

        if index_start:
            index_start = index_start.span()[0]
            # index_end = index_end.span()[1]
            data = data[index_start:75]  # 只获取流速和流向，大约取25个字符即可
            logger.info(data)
            data = data.decode('utf-8').split('\t')
            logger.info(data)
            dict = {}
            try:
                for index in config:
                    name = 'c' + str(index['serial_number'])
                    i = int(index['address'])
                    if index['divisor'] is None:
                        dict[name] = float(data[i])
                    else:
                        dict[name] = round((float(data[i]) / index['divisor']), 2)
                logger.info(dict)
                return dict
            except Exception as e:
                logger.error(e)
                return "error"
        else:
            return 'pass'
"""
