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
        "console": {
            "level": "INFO",
            "handlers": ["console", "connector_file"],
            "propagate": True,
            "qualname": "console.debug",
        },
        "sm140_file": {
            "level": "DEBUG",
            "handlers": ["console", "sm140_file"],
            "propagate": True,
            "qualname": "sm140.debug",
        },
        "wxt536_file": {
            "level": "DEBUG",
            "handlers": ["console", "wxt536_file"],
            "propagate": True,
            "qualname": "wxt536.debug",
        },
        "adcp_file": {
            "level": "DEBUG",
            "handlers": ["console", "adcp_file"],
            "propagate": True,
            "qualname": "adcp.debug",
        },
        "dandian_file": {
            "level": "DEBUG",
            "handlers": ["console", "dandian_file"],
            "propagate": True,
            "qualname": "dandian.debug",
        },
        "td266_file": {
            "level": "DEBUG",
            "handlers": ["console", "td266_file"],
            "propagate": True,
            "qualname": "td266.debug",
        },
        "shuizhi_file": {
            "level": "DEBUG",
            "handlers": ["console", "shuizhi_file"],
            "propagate": True,
            "qualname": "shuizhi.debug",
        },
    },
    handlers={
        # 数据采集程序控制台输出handler
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "connector_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/connector_log/connector_file.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "sm140_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/sm140_log/sm140_file.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "wxt536_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/wxt536_log/wxt536_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "adcp_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/adcp_log/adcp_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "dandian_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/dandian_log/dandian_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "td266_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/td266_log/td266_log.log',
            'maxBytes': 10 * 1024 * 1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 20,
            "encoding": "utf-8"
        },
        "shuizhi_file": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/shuizhi_log/shuizhi_log.log',
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
            "format": "%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S]",
            "class": "logging.Formatter",
        },
    },
)
logger = logging.getLogger("console")
sm140_file_logger = logging.getLogger("sm140_file")
wxt536_file_logger = logging.getLogger("wxt536_file")
adcp_file_logger = logging.getLogger("adcp_file")
dandian_file_logger = logging.getLogger("dandian_file")
td266_file_logger = logging.getLogger("td266_file")
shuizhi_file_logger = logging.getLogger("shuizhi_file")
