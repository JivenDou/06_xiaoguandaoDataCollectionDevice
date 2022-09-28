from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql
import traceback


class Cancel_alarm(AbstractApi):

    def operation(self, request):
        operate_mysql = OperateMysql()
        id = request['id']
        sql = "UPDATE alarm_data_tbl SET is_cancel=1 WHERE id=%s;" % (id)
        try:
            operate_mysql.execute_sql(sql)
            return "告警关闭成功"
        except:
            print(traceback.format_exc())
            return "告警关闭失败"
