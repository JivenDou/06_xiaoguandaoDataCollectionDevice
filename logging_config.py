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
        "modbus_connector": {
            "level": "INFO",
            "handlers": ["console", "modbus_connector"],
            "propagate": True,
            "qualname": "modbus_connector.debug",
        },
        "tcp_connector": {
            "level": "INFO",
            "handlers": ["console", "tcp_connector"],
            "propagate": True,
            "qualname": "tcp_connector.debug",
        },
        "sm140_converter": {
            "level": "DEBUG",
            "handlers": ["console", "sm140_converter"],
            "propagate": True,
            "qualname": "sm140_converter.debug",
        },
        "wxt536_converter": {
            "level": "DEBUG",
            "handlers": ["console", "wxt536_converter"],
            "propagate": True,
            "qualname": "wxt536_converter.debug",
        },
        "adcp_converter": {
            "level": "DEBUG",
            "handlers": ["console", "adcp_converter"],
            "propagate": True,
            "qualname": "adcp_converter.debug",
        },
        "cec21_converter": {
            "level": "DEBUG",
            "handlers": ["console", "cec21_converter"],
            "propagate": True,
            "qualname": "cec21_converter.debug",
        },
        "td266_converter": {
            "level": "DEBUG",
            "handlers": ["console", "td266_converter"],
            "propagate": True,
            "qualname": "td266_converter.debug",
        },
        "modbus_converter": {
            "level": "DEBUG",
            "handlers": ["console", "modbus_converter"],
            "propagate": True,
            "qualname": "modbus_converter.debug",
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
        "modbus_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/modbus_connector/modbus_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "tcp_connector": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/tcp_connector/tcp_connector.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "sm140_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/sm140_converter/sm140_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "wxt536_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/wxt536_converter/wxt536_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "adcp_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/adcp_converter/adcp_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "cec21_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/cec21_converter/cec21_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "td266_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/td266_converter/td266_converter.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "modbus_converter": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/modbus_converter/modbus_converter.log',
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
modbus_connector = logging.getLogger("modbus_connector")
tcp_connector = logging.getLogger("tcp_connector")
sm140_converter = logging.getLogger("sm140_converter")
wxt536_converter = logging.getLogger("wxt536_converter")
adcp_converter = logging.getLogger("adcp_converter")
cec21_converter = logging.getLogger("cec21_converter")
td266_converter = logging.getLogger("td266_converter")
modbus_converter = logging.getLogger("modbus_converter")
