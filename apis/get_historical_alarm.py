from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql
import time
import datetime

class Get_historical_alarm(AbstractApi):
    '''查询历史报警（包含已读和未读），可根据设备名、时间来进行部分查询'''

    def operation(self, request):
        operate_mysql = OperateMysql()
        device_name = request['device']
        time1 = request['begin_time']

        # 查报警
        if device_name is None and time1 is None:
            sql = "SELECT id,CAST(times AS CHAR) as times,name,data,is_cancel FROM alarm_data_tbl order by times desc;"
            res = operate_mysql.execute_sql(sql)
        elif device_name is not None and time1 is None:
            sql1 = "SELECT (serial_number) FROM data_point_tbl WHERE device_name=\'%s\';" % (device_name)
            res1 = operate_mysql.execute_sql(sql1)
            basic_datas = []
            for each in res1:
                basic_datas.append('c' + str(each['serial_number']))
            sql = "SELECT id, CAST(times AS CHAR) as times,name,data,is_cancel FROM alarm_data_tbl WHERE name in %s order by times desc;" % (format(tuple(basic_datas)))
            res = operate_mysql.execute_sql(sql)
        elif device_name is None and time1 is not None:
            begin_time = datetime.datetime.fromtimestamp(int(request['begin_time']))
            end_time = datetime.datetime.fromtimestamp(int(request['end_time']))
            sql = "SELECT id,CAST(times AS CHAR) as times,name,data,is_cancel FROM alarm_data_tbl WHERE times > \'%s\' and times < \'%s\' order by times desc;" % (begin_time, end_time)
            res = operate_mysql.execute_sql(sql)
        elif device_name is not None and time1 is not None:
            begin_time = datetime.datetime.fromtimestamp(int(request['begin_time']))
            end_time = datetime.datetime.fromtimestamp(int(request['end_time']))
            sql1 = "SELECT (serial_number) FROM data_point_tbl WHERE device_name=\'%s\';" % (device_name)
            res1 = operate_mysql.execute_sql(sql1)
            basic_datas = []
            for each in res1:
                basic_datas.append('c' + str(each['serial_number']))
            sql = "SELECT id,CAST(times AS CHAR) as times,name,data,is_cancel FROM alarm_data_tbl WHERE times > \'%s\' and times < \'%s\' and name in %s order by times desc;" % (begin_time, end_time, format(tuple(basic_datas)))
            res = operate_mysql.execute_sql(sql)


        if len(res) != 0:
            # 查报警对应的点和上下限
            list_alarm = []
            for each in res:
                serial_number = each['name'].replace('c', '')
                sql2 = "SELECT io_point_name, alarm_low_limit, alarm_up_limit FROM data_point_tbl WHERE serial_number=%s;" % (serial_number)
                res2 = operate_mysql.execute_sql(sql2)
                if len(res2) == 0:
                    io_point_name = "相关信息关联失败"
                    alarm_low_limit = "相关信息关联失败"
                    alarm_up_limit = "相关信息关联失败"
                else:
                    io_point_name = res2[0]['io_point_name']
                    alarm_low_limit = res2[0]['alarm_low_limit']
                    alarm_up_limit = res2[0]['alarm_up_limit']
                dict_alarm = {'id': each['id'], 'times': each['times'], 'io_point_name': io_point_name, 'data': each['data'], 'is_cancel': each['is_cancel'], 'alarm_low_limit': alarm_low_limit, 'alarm_up_limit': alarm_up_limit}
                list_alarm.append(dict_alarm)
            return list_alarm
        else:
            return None