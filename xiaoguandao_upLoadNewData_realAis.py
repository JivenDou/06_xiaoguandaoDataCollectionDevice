"""
@File  : xiaoguandao_upLoadNewData_realAis.py
@Author: DJW
@Date  : 2022-11-18 14:35:14
@Desc  : 向云端上传“实时数采”数据
"""
import requests
import time
import threading
from logging_config import upload_data as logger
from event_storage import EventStorage
from logging_config import LOGGING_CONFIG
import logging.config

logging.config.dictConfig(LOGGING_CONFIG)


class XiaoGuanDaoUpLoadNewDataRealAis(threading.Thread):
    def __init__(self):
        super(XiaoGuanDaoUpLoadNewDataRealAis, self).__init__()
        self._storage = EventStorage()
        self.project_name = "xiaoguandao"
        self.post_url = 'http://211.159.161.227:18000/xiaoguandao_sendDataToServer_realAis.php'
        self.table = None
        self.mmsi = None

    def run(self):
        while True:
            try:
                # 查询表名--------------------
                station_name = {"station_name": "ais"}

                self.table = f"{self.project_name}_{station_name['station_name']}_tbl"
                sql = f"SELECT * FROM {self.table} WHERE is_send = 0"
                datas = self._storage.execute_sql(sql)
                # 判空--------------------
                if datas == ():
                    logger.info(f'{self.table}查询数据为0')
                    time.sleep(10)
                    continue
                # 遍历每一条数据
                for data in datas:
                    data['times'] = str(data['times'])
                    del data['is_send']
                    # 查询若为空值，则置0--------------------
                    for k in data:
                        if data[k] is None:
                            data[k] = 'NULL'
                    # 发送数据--------------------
                    self.mmsi = data['mmsi']
                    print(data)
                    self.send_data(data)
                    time.sleep(0.001)
                # 10秒上传一组
                time.sleep(10)
            except Exception as e:
                logger.error(f"{repr(e)}")
                time.sleep(10)

    def send_data(self, data):
        try:
            # verify=False避免ssl认证
            ret = requests.post(url=self.post_url, json=data, verify=False)
            if ret.status_code == 200:
                logger.info(f'{self.table} {ret.text} {ret.status_code}')
                # 更新数据
                sql = f"UPDATE {self.table} SET is_send=1 WHERE is_send=0 AND mmsi={self.mmsi}"
                self._storage.execute_sql(sql)
            else:
                logger.error(f'{self.table} {ret.text} {ret.status_code} {data}')
        except Exception as e:
            logger.error(f"{repr(e)}")


if __name__ == '__main__':
    upload_data = XiaoGuanDaoUpLoadNewDataRealAis()
    upload_data.run()
