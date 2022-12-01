"""
@File  : xiaoguandao_upLoadNewData.py
@Author: DJW
@Date  : 2022-11-18 14:35:14
@Desc  : 向云端上传“数采”、“gps”和“ais历史”数据
"""
import requests
import time
import threading
from logging_config import upload_data as logger
from event_storage import EventStorage
# from logging_config import LOGGING_CONFIG
# import logging.config
#
# logging.config.dictConfig(LOGGING_CONFIG)


class XiaoGuanDaoUpLoadNewData(threading.Thread):
    def __init__(self):
        super(XiaoGuanDaoUpLoadNewData, self).__init__()
        self._storage = EventStorage()
        self.project_name = "xiaoguandao"
        self.post_url = 'http://211.159.161.227:18000/xiaoguandao_sendDataToServer.php'
        self.table = None
        self.data_id = None

    def run(self):
        while True:
            try:
                # 查询表名--------------------
                station_names = [{"station_name": "shucai"}, {"station_name": "ais_history"}, {"station_name": "tk009"}]
                # 获取、发送、更新数据--------------------
                data_null_flag = 0
                # 遍历shucai、tk009和ais历史表
                for station_name in station_names:
                    self.table = f"{self.project_name}_{station_name['station_name']}_tbl"
                    sql = f"SELECT * FROM {self.table} WHERE is_send = 0 LIMIT 1"
                    data = self._storage.execute_sql(sql)
                    # 判空--------------------
                    if data == ():
                        if data_null_flag < len(station_names)-1:
                            logger.info(f'{self.table}查询数据为0')
                            data_null_flag += 1
                            time.sleep(0.001)
                            continue
                        else:
                            logger.info(f'{self.table}查询数据为0')
                            time.sleep(10)
                            break

                    data = data[0]
                    data['times'] = str(data['times'])
                    del data['is_send']
                    data['station_name'] = station_name['station_name']
                    # data['project_name'] = self.project_name
                    # 查询若为空值，则置0--------------------
                    for k in data:
                        if data[k] is None:
                            data[k] = 'NULL'
                    # 发送数据--------------------
                    self.data_id = data["id"]
                    # print(data)
                    self.send_data(data)
                    time.sleep(0.001)
                # 0.01秒上传一组
                time.sleep(0.01)
            except Exception as e:
                logger.error(f"{repr(e)}")

    def send_data(self, data):
        try:
            # verify=False避免ssl认证
            ret = requests.post(url=self.post_url, json=data, verify=False)
            if ret.status_code == 200:
                logger.info(f'{self.table} {ret.text} {ret.status_code}')
                # 更新数据
                sql = f"UPDATE {self.table} SET is_send=1 WHERE is_send=0 AND id={self.data_id}"
                self._storage.execute_sql(sql)
            else:
                logger.error(f'{self.table} {ret.text} {ret.status_code} {data}')
                time.sleep(10)
        except Exception as e:
            logger.error(f"{repr(e)}")


if __name__ == '__main__':
    upload_data = XiaoGuanDaoUpLoadNewData()
    upload_data.run()
