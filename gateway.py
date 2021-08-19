import asyncio
import datetime
import json
import threading
import time

from sanic import Sanic
from sanic.response import text, json
from sanic_cors import CORS, cross_origin
from sanic import response
from multiprocessing import Process

# device import
from event_storage import EventStorage
from configuration import Configuration
from utility import Utility
from alarm import Alarm
from historical_data_storage import HistoricalDataStorage
from hard_disk_storage import HardDiskStorage
from log import Log
from api_context import ApiContext

app = Sanic(__name__)
CORS(app)
system_config = Configuration().get_system_config()
gateway_storage = EventStorage()
connector_config = gateway_storage.get_connector_config()
Utility.start_connectors(connector_config)


# config = {"ip": "127.0.0.1",
#           "username": "root",
#           "password": "root",
#           "dataBaseName": "shucai"}
# handler = HardDiskStorage(config=config, port=3306, charset='utf8')
# res = handler.get_connectors()
# print(res)


@app.route('/readReal', methods=['POST'])
async def read_point_data(request):
    list = request.json['pointList']
    dict = gateway_storage.get_real_data(list)
    return response.json(dict)


@app.route('/readHistorical', methods=['POST'])
async def read_table_data(request):
    dict = request.json
    data_list = gateway_storage.get_historical_data(dict)
    data_json = Utility.data_encoder(data_list)
    return response.text(data_json)


@app.route('/readPointInfo', methods=['POST'])
async def read_point_info(request):
    data_list = gateway_storage.get_point_info(None)
    return response.json(data_list)


@app.route('/readStatistics', methods=['POST'])
async def read_statistics_data(request):
    list = request.json['pointList']
    dict = gateway_storage.get_real_data(list)
    return response.json(dict)


@app.route('/write', methods=['POST'])
async def write_data(request):
    id = request.json["id"]
    value = request.json["value"]
    connector = request.json["device"]
    connector.send_command("zz")


@app.route('/api', methods=['POST'])
async def read_statistics_data(request):
    if len(request.json) > 0:
        list = []
        for index in range(len(request.json)):
            api_object = request.json[index]['apiObject']
            parameter = request.json[index]['parameter']
            api = ApiContext()
            api.set_api_object(api_object)
            result = api.operation(parameter)
            list.append(result)

    return response.json(list)


# def overrun_alarm(alarms):
#     print('async overrun_alarm')
#     await asyncio.sleep(.1)
#     alarms.overrun_alarm()
#
#
# async def displacement_alarm(app, alarms):
#     print('async displacement_alarm')
#     # await asyncio.sleep(.2)
#     alarms.displacement_alarm()

async def notify_server_started_after_five_seconds():
    while True:
        await asyncio.sleep(10)
        connector = Utility.available_connectors["wxt536"]
        data = "0XZRU\r\n"
        # 8:00:00-8:01:00 everyday
        a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % 8
        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")
        timeStampA = int(time.mktime(timeArray))
        timeStampB = timeStampA + 60
        if timeStampA <= int(time.time()) <= timeStampB:
            time.sleep(10)
            connector.send_command(data)


if __name__ == "__main__":
    alarm1 = Alarm()
    threading.Thread(target=alarm1.overrun_alarm).start()
    # threading.Thread(target=alarm2.displacement_alarm).start()
    historicalDataStorage = HistoricalDataStorage()
    threading.Thread(target=historicalDataStorage.run).start()
    # app.add_task(overrun_alarm(app, alarm))
    # app.add_task(displacement_alarm(app, alarm))
    # app.add_task(notify_server_started_after_five_seconds())  # 气象仪降雨量每日清零：一号打开，二号关闭，三号关闭
    app.run(host="0.0.0.0", port=8000)
# pyinstaller -F -p C:\Users\wenge\AppData\Local\Programs\Python\Python38\Lib\site-packages  gateway.spec
# pyinstaller -F -p D:\DevTools\Python38\Lib\site-packages  gateway.spec
