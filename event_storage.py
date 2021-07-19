import time
import json
import re
from memory_storage import MemoryStorage
from hard_disk_storage import HardDiskStorage
from configuration import Configuration


class EventStorage:
    def __init__(self):
        self.config = Configuration().get_system_config()
        self.memoryStorage = MemoryStorage(self.config['memoryDatabase'])
        self.hardDiskStorage = HardDiskStorage(self.config['hardDiskdataBase'])

    def get_real_data(self, keys):
        data = self.memoryStorage.get_value(keys)
        return data

    def get_historical_data(self, select_info):
        data = self.hardDiskStorage.get_table_data(select_info)
        return data

    def real_time_data_storage(self, data):
        self.memoryStorage.set_value(data)

    def historical_data_storage(self, table_name, seve_time, data):
        self.hardDiskStorage.insert_column_many(table_name, seve_time, data)

    def get_connector_config(self):
        config = self.hardDiskStorage.get_connectors()
        for station_info in config:
            station_info['connector_config'] = json.loads(station_info['connector_config'])
        return config

    def get_station_info(self, station_name):
        return self.hardDiskStorage.get_station_info(station_name)

    def get_point_info(self, keys):
        point_list = []
        if keys:
            for key in keys:
                point_list.append(re.sub("\D", "", key))
            point_tuple = tuple(point_list)
        else:
            point_tuple = None
        return self.hardDiskStorage.get_point_info(point_tuple)

    # 获取modbus命令
    def get_command_info(self, station_name):
        return self.hardDiskStorage.get_command_info(station_name)


class Networkerror(RuntimeError):
    def __init__(self, arg):
        self.args = arg
