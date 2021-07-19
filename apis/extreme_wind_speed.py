from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql
import datetime

class Extreme_wind_speed(AbstractApi):
    """返回极大风速(一定时间范围内的最大风速)"""
    def operation(self, request):
        operate_mysql = OperateMysql()
        wind_direction = request['basic_datas'][0]      # 表示风向，如c1
        wind_speed = request['basic_datas'][1]          # 表示风速，如c2

        res_wind_speed = operate_mysql.return_result(request, wind_speed.replace('c', ''))
        begin_time = res_wind_speed['begin_time']
        end_time = res_wind_speed['end_time']

        # 返回给定时间内的最大风速、最大风速对应的时间 [{'c2': 3.0, 'times': datetime.datetime(2021, 5, 4, 16, 25, 31)}]
        sql1 = "SELECT %s, times FROM %s WHERE times >= \'%s\' and times < \'%s\' ORDER BY %s desc limit 1;" % (wind_speed, res_wind_speed['table_name'], begin_time, end_time, wind_speed)
        res1 = operate_mysql.execute_sql(sql1)
        if len(res1) != 0:
            speed = res1[0][wind_speed]
            times = res1[0]['times']
            res_wind_direction = operate_mysql.return_result(request, wind_direction.replace('c', ''))
            sql3 = "SELECT %s FROM %s WHERE times = \'%s\';" % (wind_direction, res_wind_direction['table_name'], times)
            res3 = operate_mysql.execute_sql(sql3)[0][wind_direction]

            dict_res = {request['keys'][0]: res3, request['keys'][1]: speed, request['keys'][2]: times.strftime('%Y-%m-%d %H:%M:%S')}

            return dict_res
        else:
            return None
