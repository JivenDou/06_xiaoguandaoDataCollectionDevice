from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql

class Get_unread_alarm(AbstractApi):
    '''查询未读，可根据设备名来进行部分查询'''

    def operation(self, request):
        operate_mysql = OperateMysql()
        device_name = request['device']
        # 查报警
        if device_name is None:
            sql1 = "SELECT id, CAST(times AS CHAR) as times,name,data FROM alarm_data_tbl WHERE is_cancel=0 order by times desc;"
            res1 = operate_mysql.execute_sql(sql1)
        else:
            sql = "SELECT (serial_number) FROM data_point_tbl WHERE device_name=\'%s\';" % (device_name)
            res = operate_mysql.execute_sql(sql)
            basic_datas = []
            for each in res:
                basic_datas.append('c' + str(each['serial_number']))
            sql1 = "SELECT id, CAST(times AS CHAR) as times,name,data FROM alarm_data_tbl WHERE is_cancel=0 and name in %s order by times desc;" % (format(tuple(basic_datas)))
            res1 = operate_mysql.execute_sql(sql1)

        if len(res1) != 0:
            # 查报警对应的点和上下限
            list_alarm = []
            for each in res1:
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
                dict_alarm = {'id': each['id'], 'times': each['times'], 'io_point_name': io_point_name, 'data': each['data'], 'alarm_low_limit': alarm_low_limit, 'alarm_up_limit': alarm_up_limit}
                list_alarm.append(dict_alarm)
            return list_alarm
        else:
            return None