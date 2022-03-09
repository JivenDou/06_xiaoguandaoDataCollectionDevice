import json
from sanic.log import error_logger
import sys
from AES_crypt import decrypt


class Configuration:
    def __init__(self, path='config.json'):
        self.path = path

    def get_config(self):
        """"读取配置"""
        try:
            with open(self.path) as json_file:
                config = json.load(json_file)
                config['hardDiskdataBase']['password'] = decrypt(config['hardDiskdataBase']['password'])
            return config
        except FileNotFoundError as e:
            error_logger.error(f"config file does not exist:{e}")
            sys.exit()
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
