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
        "sanic.root": {
            "level": "DEBUG",
            "handlers": ["console", "custome_console"]
        },
        "sanic.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sanic.error",
        },
        "sanic.access": {
            "level": "WARNING",
            "handlers": ["access_console"],
            "propagate": True,
            "qualname": "sanic.access",
        },
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
        "access_console": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": sys.stdout,
        },
        "custome_console": {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'level': 'INFO',
            'maxBytes': 100*1024,
            'delay': True,
            "formatter": "generic",
            "backupCount": 10
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
        "access": {
            "format": "%(asctime)s - (%(name)s) [%(levelname)s][%(host)s]: "
                      + "%(request)s %(message)s %(status)d %(byte)d",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        },
    },
)
logger = logging.getLogger("sanic.root")
error_logger = logging.getLogger("sanic.error")
access_logger = logging.getLogger("sanic.access")
