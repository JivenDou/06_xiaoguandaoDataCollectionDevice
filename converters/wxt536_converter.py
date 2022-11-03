import re
from converter import Converter
from tools.format_value import format_value
from logging_config import wxt536_converter as logger


class WXT536Converter(Converter):

    def __init__(self, name):
        self._name = name

    def convert(self, config, data):
        """
        data: b'0R0,Dm=267D,Sm=1.2M,Ta=-25.0C,Ua=87.1P,Pa=1001.9H,Rc=-0.00M,Th=28.3C,Vh=0.0#'
        """
        logger.info(f"原始接收数据[{self._name}]: {data}")
        if data:
            dict = {}
            try:
                list = data.decode().split(",")
                logger.info(f"({self._name})解码分割后， 标准长度:9，实际长度:{len(list)}, 内容: {list}, ")
                if list[0] == '0R0':
                    for index in config:
                        name = 'c' + str(index['serial_number'])
                        i = int(index['address'])
                        value = None
                        if list[i][-1] != "#":
                            value = re.findall(r"-*\d+\.?\d*", list[i])[0]
                        dict[name] = format_value(index, value)
                    logger.info(f"({self._name})解析后数据：{dict}")
                    return dict
                elif len(list) > 0:
                    return "pass"
                else:
                    return "error"
            except Exception as e:
                logger.error(f"({self._name}):{repr(e)}")
                return "error"
