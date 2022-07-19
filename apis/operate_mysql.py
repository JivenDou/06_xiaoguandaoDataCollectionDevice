import pymysql
import traceback
import time
import datetime
from configuration import Configuration
from AES_crypt import decrypt


class OperateMysql():
    config = Configuration().get_config()
    config = config["hardDiskdataBase"]

    def __init__(self, config=config, port=3306, charset='utf8'):
        self.host = config['ip']
        self.user = config['username']
        self.passwd = decrypt(config['password'])
        self.db = config['dataBaseName']
        self.port = port
        self.charset = charset
        self.conn = None
        self._conn()

    def _conn(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, db=self.db, port=self.port, autocommit=True)
            return True
        except Exception as e:
            print(e)
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

    def execute_sql(self, sql):
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

    def return_result(self, point_statistic, serial_number):
        # "parameter":{"key": "s2", "basic_data": "c2", "begin_time": "1618389390", "end_time": "1618389572"}
        begin_time = datetime.datetime.fromtimestamp(int(point_statistic['begin_time']))
        end_time = datetime.datetime.fromtimestamp(int(point_statistic['end_time']))
        sql = "SELECT device_name FROM data_point_tbl WHERE serial_number=%s;" % (serial_number)
        res = self.execute_sql(sql)
        table_name = 'table_' + res[0]['device_name']
        dict_res = {"table_name": table_name, "begin_time": begin_time, "end_time": end_time}

        return dict_res

# def database_parameters(self):
#     config = {'ip': 'localhost', 'username': 'rootroot', 'password': 'rootroot', 'dataBaseName': 'shucai'}
#     self.config = config
