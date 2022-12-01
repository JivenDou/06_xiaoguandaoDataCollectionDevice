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
        "http_connector": {
            "level": "INFO",
            "handlers": ["console", "http_connector"],
            "propagate": True,
            "qualname": "http_connector.debug",
        },
        "tk009_http_connector": {
            "level": "INFO",
            "handlers": ["console", "tk009_http_connector"],
            "propagate": True,
            "qualname": "tk009_http_connector.debug",
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
        "ais_converter": {
            "level": "DEBUG",
            "handlers": ["console", "ais_converter"],
            "propagate": True,
            "qualname": "ais_converter.debug",
        },
        "tk009_converter": {
            "level": "DEBUG",
            "handlers": ["console", "tk009_converter"],
            "propagate": True,
            "qualname": "tk009_converter.debug",
        },
        "upload_data": {
            "level": "DEBUG",
            "handlers": ["console", "upload_data"],
            "propagate": True,
            "qualname": "upload_data.debug",
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
        "http_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/http_connector/http_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "tk009_http_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/tk009_http_connector/tk009_http_connector.log',
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
        "ais_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/ais_converter/ais_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "tk009_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/tk009_converter/tk009_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "upload_data": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/upload_data/upload_data.log',
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
http_connector = logging.getLogger("http_connector")
tk009_http_connector = logging.getLogger("tk009_http_connector")
ais_http_connector = logging.getLogger("ais_http_connector")
shucai_converter = logging.getLogger("shucai_converter")
ais_converter = logging.getLogger("ais_converter")
tk009_converter = logging.getLogger("tk009_converter")
upload_data = logging.getLogger("upload_data")
