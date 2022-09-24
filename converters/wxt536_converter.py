from logging_config import logger
import re
from converter import Converter


class WXT536Converter(Converter):
    """
    data: b'0R0,Dm=267D,Sm=1.2M,Ta=-25.0C,Ua=87.1P,Pa=1001.9H,Rc=-0.00M,Th=28.3C,Vh=0.0#'
    """

    def convert(self, config, data):
        logger.info(f"(气象仪)原始接收数据: {data}")
        if data:
            dict = {}
            try:
                list = data.decode().split(",")
                logger.info(f"(气象仪)解码分割后， 标准长度:9，实际长度:{len(list)}, 内容: {list}, ")
                if list[0] == '0R0':
                    for index in config:
                        name = 'c' + str(index['serial_number'])
                        i = int(index['address'])
                        value = None
                        if list[i][-1] != "#":
                            value = re.findall(r"-*\d+\.?\d*", list[i])[0]
                        dict[name] = format_value(index, value)
                    logger.info(f"(气象仪)解析后数据：{dict}")
                    return dict
                elif len(list) > 0:
                    return "pass"
                else:
                    return "error"
            except Exception as e:
                logger.error(e)
                return "error"


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
        if low_limit <= value <= up_limit:
            return value
        else:
            return ''
    else:
        return ''
