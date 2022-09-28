from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql


class Min_from_database(AbstractApi):

    def operation(self, request):
        operate_mysql = OperateMysql()
        basic_data = request['basic_data']
        serial_number = basic_data.replace('c', '')
        res1 = operate_mysql.return_result(request, serial_number)
        sql1 = "SELECT %s, CAST(times AS CHAR) as times FROM %s WHERE times > \'%s\' and times < \'%s\' ORDER BY %s limit 1;" % (
        basic_data, res1['table_name'], res1['begin_time'], res1['end_time'], basic_data)
        res2 = operate_mysql.execute_sql(sql1)
        if len(res2) != 0:
            res = {request['keys'][0]: res2[0][basic_data], request['keys'][1]: res2[0]['times']}
            return res
        else:
            return None
