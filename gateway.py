import asyncio
import datetime
import sys
import time
import os
import wmi
from sanic import Sanic
from sanic_cors import CORS
from sanic import response

# device import
from event_storage import EventStorage
from configuration import Configuration
from utility import Utility
from alarm import Alarm
from historical_data_storage import HistoricalDataStorage
from api_context import ApiContext
from AES_crypt import decrypt
from logging_config import LOGGING_CONFIG
import logging.config
from xiaoguandao_upLoadNewData import XiaoGuanDaoUpLoadNewData
from xiaoguandao_upLoadNewData_realAis import XiaoGuanDaoUpLoadNewDataRealAis

# logging config
logging.config.dictConfig(LOGGING_CONFIG)
handlers = LOGGING_CONFIG['handlers']
for handler in handlers:
    item = handlers[handler]
    if 'filename' in item:
        filename = item['filename']
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
# --------------------------
gateway_storage = EventStorage()
connector_config = gateway_storage.get_connector_config()
Utility.start_connectors(connector_config)
app = Sanic(__name__)
# app.config.CORS_ORIGINS = "*"
CORS(app)

#
# @app.route('/readReal', methods=['POST'])
# async def read_point_data(request):
#     list = request.json['pointList']
#     dict = gateway_storage.get_real_data(list)
#     return response.json(dict)
#
#
# @app.route('/readHistorical', methods=['POST'])
# async def read_table_data(request):
#     dict = request.json
#     data_list = gateway_storage.get_historical_data(dict)
#     data_json = Utility.data_encoder(data_list)
#     return response.text(data_json)
#
#
# # 历史数据库分页查询接口--------------------------------------------\\
# @app.post('/getTotalNumber')
# async def get_total_number(request):
#     dict = request.json
#     data_list = gateway_storage.get_total_count_and_first_id(dict)
#     return response.json(data_list)
#
#
# @app.post("/getItem")
# def get_one_page_content(request):
#     dict = request.json
#     data_list = gateway_storage.get_item_by_id_offset(dict)
#     data_json = Utility.data_encoder(data_list)
#     return response.text(data_json)
#
#
# # 历史数据导出接口--------------------------------------------\\
# @app.post('/quary')
# async def quary_table_data(request):
#     dict = request.json
#     res = gateway_storage.quary_table_data(dict)
#     if not res:
#         return response.text("查询参数错误")
#     return response.json({"filename": res})
#
#
# @app.route("/download")
# async def downlod_file(request):
#     filename = request.args.get("filename")
#     if sys.platform == 'win32':
#         filepath = './' + filename
#     elif sys.platform == 'linux':
#         filepath = filename
#     return await response.file_stream(
#         filepath,
#         chunk_size=1024,
#         filename=filename
#     )
#
#
# @app.route('/readPointInfo', methods=['POST'])
# async def read_point_info(request):
#     data_list = gateway_storage.get_point_info(None)
#     return response.json(data_list)
#
#
# # @app.route('/readStatistics', methods=['POST'])
# # async def read_statistics_data(request):
# #     list = request.json['pointList']
# #     dict = gateway_storage.get_real_data(list)
# #     return response.json(dict)
# #
# #
# # @app.route('/write', methods=['POST'])
# # async def write_data(request):
# #     id = request.json["id"]
# #     value = request.json["value"]
# #     connector = request.json["device"]
# #     connector.send_command("zz")
#
#
# @app.route('/api', methods=['POST'])
# async def read_statistics_data(request):
#     if len(request.json) > 0:
#         list = []
#         for index in range(len(request.json)):
#             api_object = request.json[index]['apiObject']
#             parameter = request.json[index]['parameter']
#             api = ApiContext()
#             api.set_api_object(api_object)
#             result = api.operation(parameter)
#             list.append(result)
#
#     return response.json(list)
#
#
# # def verify_cpu_code():
# #     # 获取配置文件中CPU序列号
# #     config_handle = Configuration()
# #     config = config_handle.get_system_config()
# #     cpu_code_from_config_file = config['code']
# #     # 获取当前设备CPU序列号
# #
# #
# #     # 判断是否匹配
# #     if cpu_code == cpu_code_from_config_file:
# #         return True
# #     else:
# #         return False
#
#
# @app.post('/verify')
# def verify_app(request):
#     config = Configuration().get_config()
#     for cpu in wmi.WMI().Win32_Processor():
#         cpu_code = cpu.ProcessorId.strip()
#     de_cpu_code = decrypt(config['activation_code'])
#     if cpu_code == de_cpu_code:
#         return response.json({'status': 'yes'})
#     else:
#         return response.json({'status': 'no'})
#
#
# @app.post('/activate')
# def acvivate(request):
#     activate_code = request.json['code']
#     for cpu in wmi.WMI().Win32_Processor():
#         cpu_code = cpu.ProcessorId.strip()
#     de_activate_code = decrypt(activate_code)
#     if de_activate_code == cpu_code:
#         config = Configuration()
#         res = config.set_config(**{"activation_code": activate_code})
#         if res:
#             return response.json({'status': 'yes'})
#     return response.json({'status': 'no'})
#
#
# # def overrun_alarm(alarms):
# #     print('async overrun_alarm')
# #     await asyncio.sleep(.1)
# #     alarms.overrun_alarm()
# #
# #
# # async def displacement_alarm(app, alarms):
# #     print('async displacement_alarm')
# #     # await asyncio.sleep(.2)
# #     alarms.displacement_alarm()
#
# async def notify_server_started_after_five_seconds():
#     while True:
#         await asyncio.sleep(10)
#         if 'wxt536' not in Utility.available_connectors:
#             break
#         connector = Utility.available_connectors["wxt536"]
#         data = "0XZRU\r\n"
#         # 8:00:00-8:01:00 everyday
#         a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % 8
#         timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
#         timeStampA = int(time.mktime(timeArray))
#         timeStampB = timeStampA + 60
#         if timeStampA <= int(time.time()) <= timeStampB:
#             time.sleep(10)
#             connector.send_command(data)


if __name__ == "__main__":
    # Alarm().start()
    HistoricalDataStorage().start()
    # 实时上传云服务器
    XiaoGuanDaoUpLoadNewData().start()
    XiaoGuanDaoUpLoadNewDataRealAis().start()

    # 气象仪降雨量每日清零：一号打开，二号关闭，三号关闭
    # app.add_task(notify_server_started_after_five_seconds())
    # app.run(host="0.0.0.0", port=8000)
