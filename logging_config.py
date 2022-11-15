"""
@File  : log_config.py
@Author: lee
@Date  : 2022/7/13/0013 11:08:55
@Desc  :
"""
import logging
import sys

LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        # 新曾自定义日志，用于数据采集程序
        "general": {
            "level": "INFO",
            "handlers": ["console", "general"],
            "propagate": True,
            "qualname": "general.debug",
        },
        "ais_http_connector": {
            "level": "INFO",
            "handlers": ["console", "ais_http_connector"],
            "propagate": True,
            "qualname": "ais_http_connector.debug",
        },
        "shucai_converter": {
            "level": "DEBUG",
            "handlers": ["console", "shucai_converter"],
            "propagate": True,
            "qualname": "shucai_converter.debug",
        },
    },
    handlers={
        # 数据采集程序控制台输出handler
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "general": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/general/general.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "ais_http_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/ais_http_connector/ais_http_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "shucai_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/shucai_converter/shucai_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
    },
    formatters={
        # 自定义文件格式化器
        "generic": {
            "format": "%(asctime)s {%(process)d(%(thread)d)} [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
            "class": "logging.Formatter",
        },
    },
)
general = logging.getLogger("general")
ais_http_connector = logging.getLogger("ais_http_connector")

shucai_converter = logging.getLogger("shucai_converter")
