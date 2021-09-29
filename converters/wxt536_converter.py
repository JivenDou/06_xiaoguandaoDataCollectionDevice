import json
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
        if data:
            dict = {}
            try:
                list = data.decode().split(",")
                if len(list) == 9:
                    for index in config:
                        name = 'c' + str(index['serial_number'])
                        i = int(index['address'])
                        if list[i][-1] != "#":
                            dict[name] = re.findall(r"\d+\.?\d*", list[i])[0]
                        else:
                            dict[name] = "null"
                    return dict
                elif len(list) > 0:
                    return "pass"
                else:
                    return "error"
            except Exception as e:
                print(e)
                return "error"
