import pymysql
import traceback
import time
from log import Log


class HardDiskStorage():
    def __init__(self, config, port=3306, charset='utf8'):
        self.host = config['ip']
        self.user = config['username']
        self.passwd = config['password']
        self.db = config['dataBaseName']
        self.port = port
        self.charset = charset
        self.conn = None
        self._conn()
        self.log = Log()

    def _conn(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, database=self.db, port=self.port, autocommit=True)
            return True
        except Exception as e:
            return False

    def _reConn(self, num=28800, stime=3):  # 重试连接总次数为1天,这里根据实际情况自己设置,如果服务器宕机1天都没发现就......
        _number = 0
        _status = True
        while _status and _number <= num:
            try:
                self.conn.ping()  # cping 校验连接是否异常
                _status = False
            except:
                if self._conn() == True:  # 重新连接,成功退出
                    _status = False
                    break
                _number += 1
                time.sleep(stime)  # 连接不成功,休眠3秒钟,继续循环，知道成功或重试次数结束

    def get_station_info(self, station_name):
        sql = "SELECT * FROM data_point_tbl where station_name = '%s'" % station_name
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return False

    def get_point_info(self, point_tuple):
        if point_tuple:
            sql = "SELECT * FROM data_point_tbl where serial_number in %s" % (str(point_tuple))
        else:
            sql = "SELECT * FROM data_point_tbl"
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return False

    def get_table_data(self, senect_info):
        table_name = "table_" + senect_info['deviceName']
        time_begin = senect_info['timeBegin']
        time_end = senect_info['timeEnd']
        column = senect_info['pointList']
        if len(column) > 0:
            sql = "SELECT times"
            for column_name in column:
                sql = sql + "," + column_name
            sql = sql + " FROM %s WHERE times > '%s' AND times < '%s'" % (table_name, time_begin, time_end)
        else:
            sql = "SELECT * FROM %s WHERE times > '%s' AND times < '%s';" % (table_name, time_begin, time_end)
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return None

    def get_connectors(self):
        sql = "SELECT * FROM station_info_tbl WHERE status = 1"
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return None

    def create_delete_stale_data_event(self, eventName, table_name, day):
        self.cursor = self.conn.cursor()
        sql = "create event %s on SCHEDULE every 1 day do delete from %s where times<(CURRENT_TIMESTAMP() + INTERVAL -%s DAY);" % (
            eventName, table_name, day)
        self.cursor.execute(sql)
        self.cursor.close()

    def create_many_column_table(self, table_name, list):
        self.cursor = self.conn.cursor()
        for index in range(len(list)):
            dataType = list[index]['storageType']
            columnName = "c" + str(list[index]['serialNumber'])
            sql_c = "CREATE TABLE IF NOT EXISTS %s (times datetime NOT NULL,INDEX (times)) \
                ENGINE=InnoDB DEFAULT CHARSET=utf8;" % (table_name)
            sql_add = "ALTER TABLE %s ADD %s %s " % (table_name, columnName, dataType)
            try:
                self.cursor.execute(sql_c)
                self.cursor.execute(sql_add)
            except:
                print(traceback.format_exc())
        sql_send = "ALTER TABLE %s ADD 'is_send'tinyint NOT NULL DEFAULT '0'" % (table_name)
        self.cursor.execute(sql_send)
        self.cursor.close()

    def insert_column_many(self, table_name, timeNow, dict):
        try:
            self.cursor = self.conn.cursor()
            sql = "INSERT INTO %s (times" % (table_name)
            for key_name in dict.keys():
                sql = sql + "," + key_name
            sql = sql + ") VALUE ('" + str(timeNow) + "'"
            for key_name in dict.keys():
                data = "," + str(dict[key_name])
                sql = sql + data
            sql = sql + ")"
            try:
                self.cursor.execute(sql)
                # 提交到数据库执行
                self.conn.commit()
            except Exception as e:
                # 如果发生错误则回滚
                self.conn.rollback()
                print(e)
        except Exception as e:
            self._reConn()
            print(e)
        else:
            self.cursor.close()

    def close(self):
        self.conn.close()

    def get_command_info(self, station_name):
        sql = "SELECT command FROM command where station_name = '%s' " % station_name
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return None

    # lee
    def get_device_name_by_station_name(self, station_name):
        sql = "SELECT DISTINCT device_name FROM data_point_tbl WHERE station_name = '%s' " % station_name
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return None

    def get_data_point_by_device_name(self, device_name):
        sql = "SELECT * FROM data_point_tbl WHERE device_name = '%s'" % device_name
        try:
            self._reConn()
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            self.cursor.close()
            return results
        except:
            print(traceback.format_exc())
            return None
