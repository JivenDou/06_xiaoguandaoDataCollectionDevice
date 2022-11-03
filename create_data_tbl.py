"""
@Date  :2021/5/21/00219:10:57
@Desc  :此类可以根据站表和点表的内容自动创建table开头的存储历史数据的数据表
        运行只对status为1的站点所对应的数据表有修改。

"""
import os
import sys

from event_storage import EventStorage
import threading


class CreateDataTable(threading.Thread):
    def __init__(self):
        super().__init__()
        self.storage = EventStorage()

    def get_stations_info(self):
        """
        获取激活的站点信息
        """
        sql = "SELECT * FROM station_info_tbl WHERE status = 1;"
        res = self.storage.execute_sql(sql)
        return res

    def get_device_by_station_name(self, station_name):
        sql = "select DISTINCT (device_name) from data_point_tbl where station_name = '%s'" % station_name
        results = self.storage.execute_sql(sql)
        return results

    def get_point_by_device_name(self, device_name):
        sql = "SELECT * FROM data_point_tbl WHERE device_name = '%s'" % device_name
        results = self.storage.execute_sql(sql)
        return results

    def run(self):
        stations_list = self.get_stations_info()
        for each_station in stations_list:
            devices_list = self.get_device_by_station_name(each_station['station_name'])
            for each_device in devices_list:
                points_list = self.get_point_by_device_name(each_device['device_name'])
                table_name = 'table_' + each_device['device_name']
                sql_c = "CREATE TABLE IF NOT EXISTS %s (id bigint primary key auto_increment, times datetime NOT NULL,INDEX (times)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_name
                self.storage.execute_sql(sql_c)
                for i in points_list:
                    dataType = i['storage_type']
                    columnName = "c" + str(i['serial_number'])
                    sql = "SELECT * FROM information_schema.COLUMNS WHERE column_name='%s' and table_name='%s' and table_schema='shucai'" % (columnName, table_name)
                    res = self.storage.execute_sql(sql)
                    if not res:
                        sql_add = "ALTER TABLE %s ADD COLUMN %s  %s comment '%s' " % (table_name, columnName, dataType, i['io_point_name'])
                        self.storage.execute_sql(sql_add)
                sql = "SELECT * FROM information_schema.COLUMNS WHERE column_name='is_send' and table_name='%s' and table_schema='shucai'" % (table_name)
                res = self.storage.execute_sql(sql)
                if not res:
                    sql_add_is_send = "ALTER TABLE %s ADD COLUMN is_send tinyint" % (table_name)
                    self.storage.execute_sql(sql_add_is_send)
                print(table_name, "done !")


if __name__ == '__main__':
    CreateDataTable().run()
