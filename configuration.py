import json
import logging
import os
import sys
import base64

import pyDes


def DesEncrypt(string):
    Des_Key = "u357asdu"  # Key
    Des_IV = "u357asdu"  # 自定IV向量
    string = base64.b64decode(string)
    k = pyDes.des(Des_Key, pyDes.CBC, Des_IV, pad=None,
                  padmode=pyDes.PAD_PKCS5)
    decryptStr = k.decrypt(string)
    return decryptStr


class Configuration:
    def __init__(self, path='config.json'):
        self.path = path

    def get_config(self):
        """"读取配置"""
        try:
            with open(self.path) as json_file:
                config = json.load(json_file)
            return config
        except FileNotFoundError as e:
            logging.error("find config file failed:", e)
            return None
        # 解密密码和序列号
        # config['hardDiskdataBase']['password'] = DesEncrypt(
        #     config['hardDiskdataBase']['password']).decode('utf-8')
        # config['code'] = DesEncrypt(config['code']).decode('utf-8')

    def set_config(self):
        pass

    def add_device(self):
        pass

    def delete_device(self):
        pass

    def updata_device(self):
        pass


if __name__ == '__main__':
    config = Configuration().get_config()
    print(config)
