from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql
import traceback

class Change_alarm_limit(AbstractApi):

    def operation(self, request):
        operate_mysql = OperateMysql()
        id = request['id']
        alarm_low_limit = request['alarm_low_limit']
        alarm_up_limit = request['alarm_up_limit']
        sql = "UPDATE data_point_tbl SET alarm_low_limit=%s, alarm_up_limit=%s WHERE id=%s" % (alarm_low_limit, alarm_up_limit, id)
        try:
            operate_mysql.execute_sql(sql)
            return "报警上下限修改成功"
        except:
            print(traceback.format_exc())
            return "报警上下限修改失败"