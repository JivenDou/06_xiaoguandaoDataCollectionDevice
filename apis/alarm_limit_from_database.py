from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql

class Alarm_limit_from_database(AbstractApi):

    def operation(self, request):
        operate_mysql = OperateMysql()
        device_name = request['device']
        if device_name is None:
            sql = "SELECT id,io_point_name,alarm_low_limit,alarm_up_limit FROM data_point_tbl WHERE alarm_low_limit IS NOT Null AND alarm_up_limit IS NOT Null;"
            res = operate_mysql.execute_sql(sql)
        else:
            sql = "SELECT id,io_point_name,alarm_low_limit,alarm_up_limit FROM data_point_tbl WHERE alarm_low_limit IS NOT Null AND alarm_up_limit IS NOT Null AND device_name=\'%s\';" % (device_name)
            res = operate_mysql.execute_sql(sql)

        return res