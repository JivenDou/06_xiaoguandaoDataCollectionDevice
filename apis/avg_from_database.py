from abstract_api import AbstractApi
from apis.operate_mysql import OperateMysql

class Avg_from_database(AbstractApi):
    
    def operation(self, request):
        operate_mysql = OperateMysql()
        basic_data = request['basic_data']
        serial_number = basic_data.replace('c', '')
        res1 = operate_mysql.return_result(request, serial_number)
        sql = "SELECT avg(%s) FROM %s WHERE times > \'%s\' and times < \'%s\';" % (basic_data, res1['table_name'], res1['begin_time'], res1['end_time'])
        res2 = operate_mysql.execute_sql(sql)
        avg_value = res2[0]['avg(' + basic_data + ')']
        if avg_value is None:
            return None
        else:
            res = {request['key']: ("%.2f" % avg_value)}
            return res