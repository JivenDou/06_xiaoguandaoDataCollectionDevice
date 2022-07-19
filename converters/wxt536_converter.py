from sanic.log import logger
import re
from converter import Converter


class WXT536Converter(Converter):
    '''
            [{"name":"c1","addr":"1"},
          {"name":"c2","addr":"2"},
          {"name":"c3","addr":"3"},
          {"name":"c4","addr":"4"},
          {"name":"c5","addr":"5"},
          {"name":"c6","addr":"6"}]
    '''

    def convert(self, config, data):
        logger.info(f"data: {data}")
        if data:
            dict = {}
            try:
                list = data.decode().split(",")
                logger.info(f"list: {list}, len: {len(list)}")
                if len(list) == 9:
                    for index in config:
                        name = 'c' + str(index['serial_number'])
                        i = int(index['address'])
                        if list[i][-1] != "#":
                            dict[name] = re.findall(r"\d+\.?\d*", list[i])[0]
                        else:
                            dict[name] = "null"
                    logger.info(f"解析后数据(气象传感器)：{dict}")
                    return dict
                elif len(list) > 0:
                    return "pass"
                else:
                    return "error"
            except Exception as e:
                logger.error(e)
                return "error"
