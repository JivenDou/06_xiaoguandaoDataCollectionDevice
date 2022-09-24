import time
import traceback
import pymysql


class Mysql:
    def __init__(self, host='', user='', passwd='', db='', port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        self.cursor = None
        self._conn()

    def _conn(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, db=self.db, port=self.port)
            self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            return True
        except Exception as e:
            print(e)
            return False

    def run(self):
        self.create_data_table()

    def get_stations_info(self):
        sql = "SELECT * FROM station_info_tbl WHERE status = 1;"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def get_device_by_station_name(self, station_name):
        sql = "select DISTINCT (device_name) from data_point_tbl where station_name = '%s'" % station_name
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def get_point_by_device_name(self, device_name):
        sql = "SELECT * FROM data_point_tbl WHERE device_name = '%s'" % device_name
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def create_data_table(self):
        stations_list = self.get_stations_info()
        for each_station in stations_list:
            devices_list = self.get_device_by_station_name(each_station['station_name'])
            for each_device in devices_list:
                points_list = self.get_point_by_device_name(each_device['device_name'])
                print(points_list)
                print("------------")
                table_name = 'table_' + each_device['device_name']
                sql_c = "CREATE TABLE IF NOT EXISTS %s (id bigint primary key , times datetime NOT NULL,INDEX (times)) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_name
                self.cursor.execute(sql_c)
                for i in points_list:
                    dataType = i['storage_type']
                    columnName = "c" + str(i['serial_number'])
                    sql_add = "ALTER TABLE %s ADD %s  %s comment '%s'" % (table_name, columnName, dataType, i['io_point_name'])
                    print(f"sql_add: {sql_add}")
                    self.cursor.execute(sql_add)
                print(table_name, "done !")


if __name__ == '__main__':
    Mysql(host='127.0.0.1', user='root', passwd='zzZZ4144670..', db='shucai').run()
