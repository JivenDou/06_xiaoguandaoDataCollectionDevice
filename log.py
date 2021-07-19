import os
import sys
import time
import logging
import logging.handlers
import inspect

current_path = os.getcwd()  # 获取当前项目路径
log_path = os.path.join(current_path, r'gateway-Log')  # 拼接日志文件存储目录
if not os.path.exists(log_path):  # 不存在则创建日志文件存储目录
    os.mkdir(log_path)
# 创建日志等级和文件映射字典
handlers = {logging.ERROR: os.path.join(log_path, r'log_error.log'),
            logging.DEBUG: os.path.join(log_path, r'log_debug.log'),
            logging.INFO: os.path.join(log_path, r'log_info.log')}


def createHandlers():
    logLevels = handlers.keys()
    for level in logLevels:
        path = os.path.abspath(handlers[level])
        # 设定每个日志文件大小，单位B
        logsize = 1024 * 1024 * 20
        # 设定保存的日志文件个数
        lognum = 50
        handlers[level] = logging.handlers.RotatingFileHandler(path, maxBytes=logsize, backupCount=lognum)


# 加载模块时创建全局变量
createHandlers()


class Log(object):
    '''
    该日志类可以把不同级别的日志输出到不同的日志文件中
    '''

    def __init__(self, level=logging.NOTSET):
        self.__loggers = {}
        logLevels = handlers.keys()
        for level in logLevels:
            logger = logging.getLogger(str(level))
            # 如果不指定level，获得的handler似乎是同一个handler?
            logger.addHandler(handlers[level])
            logger.setLevel(level)
            self.__loggers.update({level: logger})

    def printfNow(self):
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    def getLogMessage(self, level, message):
        frame, filename, lineNo, functionName, code, unknowField = inspect.stack()[2]
        '''日志格式: [时间] 文件路径-日志级别 [行号]: 具体信息'''
        res = "[%s] %s-%s [%s]:%s" % (self.printfNow(), filename, level, lineNo, message)
        return res

    def info(self, message):
        message = self.getLogMessage("info", message)
        self.__loggers[logging.INFO].info(message)

    def error(self, message):
        message = self.getLogMessage("error", message)
        self.__loggers[logging.ERROR].error(message)

    def debug(self, message):
        message = self.getLogMessage("debug", message)
        self.__loggers[logging.DEBUG].debug(message)
