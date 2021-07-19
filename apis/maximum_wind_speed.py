from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql
import datetime

class Maximum_wind_speed(AbstractApi):
    """返回最大风速（给定时段内的每隔10分钟的平均风速中的最大值）"""
    def operation(self, request):
        operate_mysql = OperateMysql()
        wind_direction = request['basic_datas'][0]      # 风向，如c1
        wind_speed = request['basic_datas'][1]          # 风速，如c2

        res_wind_speed = operate_mysql.return_result(request, wind_speed.replace('c', ''))
        begin_time = res_wind_speed['begin_time']
        end_time = res_wind_speed['end_time']

        count = (int(request['end_time']) - int(request['begin_time'])) / 600
        max_speed = 0
        status = 0      # 状态，用于判断所查询的时间段内是否有数据
        while count > 0:
            time1 = begin_time+datetime.timedelta(minutes=10)

            sql1 = "SELECT avg(%s) FROM %s WHERE times >= \'%s\' and times < \'%s\';" % (wind_speed, res_wind_speed['table_name'], begin_time, time1)
            res1 = operate_mysql.execute_sql(sql1)
            speed = res1[0]["avg(" + wind_speed + ")"]
            if speed is not None:
                status = 1  # 如果有数据，修改status，进行下一步查询
                if speed > max_speed:
                    max_speed = speed
                    return_begin_time = begin_time
                    return_end_time = time1

            count = count - 1
            begin_time = time1
        if status == 1:
            res_wind_direction = operate_mysql.return_result(request, wind_direction.replace('c', ''))
            sql2 = "SELECT avg(%s) FROM %s WHERE times >= \'%s\' and times < \'%s\';" % (wind_direction, res_wind_direction['table_name'], return_begin_time, return_end_time)
            res2 = operate_mysql.execute_sql(sql2)
            max_wind_direction = res2[0]['avg(' + wind_direction + ')']

            res = {request['keys'][0]: ("%.2f" % max_wind_direction), request['keys'][1]: ("%.2f" % max_speed), request['keys'][2]: return_begin_time.strftime('%Y-%m-%d %H:%M:%S')}

            return res
        else:
            return None