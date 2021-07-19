from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql

class Flow_direction_radar_chart(AbstractApi):
    
    def operation(self, request):
        data_dict = {}
        operate_mysql = OperateMysql()
        table_name = "table_" + request['deviceName']
        limit = request['limit']
        speed = request['speed']
        direction = request['direction']
        sql = "SELECT * FROM %s order by times desc limit %s" % (table_name, limit)
        res = operate_mysql.execute_sql(sql)

        if len(res) != 0:
            for index in res:
                for s in speed:
                    data_dict.setdefault('direction_list', []).append(index[s])
                for d in direction:
                    data_dict.setdefault('speed_list', []).append(index[d])

            return data_dict
        else:
            return None