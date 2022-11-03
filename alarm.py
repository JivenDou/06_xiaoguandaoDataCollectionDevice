"""
@Date  :2021/5/21/00219:10:57
@Desc  :
"""
from logging_config import general as logger
import threading
import time
from event_storage import EventStorage


class Alarm(threading.Thread):
    def __init__(self):
        super(Alarm, self).__init__()
        self._storage = EventStorage()
        self._save_frequency = 5
        self._last_save_time = 0

    def run(self) -> None:
        self.overrun_alarm()

    def get_real_time_data(self):
        """
        :return: data_dict {'c1': '064', 'c2': '0.1', 'c3': '20.3', 'c4': '43.2', 'c5': '1025.1', 'c6': '0.25', 'c81': '29.823', 'c82': '104.507', 'c83': '253.153'...}
        """
        point_info = self._storage.hardDiskStorage.get_point_info(point_tuple=None)
        keys_list = []
        for index in point_info:
            keys_list.append('c' + str(index['serial_number']))
        data_dict = self._storage.memoryStorage.get_value(keys_list)
        return data_dict

    def get_point_table(self):
        """
        获取所有点的点表，并增加alarm_status属性
        :return: point_info 字典组成的列表
        """
        point_info = self._storage.hardDiskStorage.get_point_info(point_tuple=None)
        for obj in point_info:
            obj['alarm_status'] = 0
        return point_info

    def update_point_table(self, point_info):
        """
        更新点表，主要更新报警上限和报警下限
        :param point_info: 更新前的点表
        :return: 更新后的点表
        """
        new = self._storage.hardDiskStorage.get_point_info(point_tuple=None)
        for i in range(0, len(new)):
            point_info[i]['alarm_low_limit'] = new[i]['alarm_low_limit']
            point_info[i]['alarm_up_limit'] = new[i]['alarm_up_limit']

    # 越限报警
    def overrun_alarm(self):
        logger.info('Over run alarm module is running!')
        try:
            point_info = self.get_point_table()
            while 1:
                self.update_point_table(point_info)
                data_dict = self.get_real_time_data()
                for index in point_info:
                    key = 'c' + str(index['serial_number'])
                    if data_dict[key]:  # 数据不为空且报警状态为零
                        data_dict[key] = float(data_dict[key])
                        if index['alarm_low_limit'] is None or index['alarm_up_limit'] is None:  # 未设置报警限值
                            continue
                        elif index['alarm_low_limit'] <= data_dict[key] <= index['alarm_up_limit']:  # 在合理范围内
                            index['alarm_status'] = 0
                        else:  # 数据越限
                            if index['alarm_status'] == 0:  # alarm_status == 0：表示第一次报警，存储报警信息
                                alarm_unit = {'name': "'" + key + "'", 'data': data_dict[key]}
                                table_name = "alarm_data_tbl"  # 报警存储表名，可以通过配置文件配置
                                alarm_time = time.strftime("%Y-%m-%d %H:%M:%S")
                                self._storage.hardDiskStorage.insert_column_many(table_name, alarm_time, alarm_unit)
                                index['alarm_status'] = 1
                            elif index['alarm_status'] == 1:  # alarm_status == 1：表示本次报警期间非第一次检测的越限
                                continue
                time.sleep(1)
        except Exception as e:
            logger.error(e)

    def overrun_alarm_storage(self, table_name, save_time, item):
        pass

    # 变位报警
    def displacement_alarm(self):
        logger.info('[displacement_alarm] - Displacement alarm module is running!')
        point_info = self._storage.hardDiskStorage.get_point_info(point_tuple=None)

        keys_list = []
        for index in point_info:
            keys_list.append('c' + str(index['serial_number']))
        last_data_dict = self._storage.memoryStorage.get_value(keys_list)

        while 1:
            now_data_dict = self._storage.memoryStorage.get_value(keys_list)
            for index in point_info:
                key = 'c' + str(index['serial_number'])
                if index['signal_type'] == 'Switch' and now_data_dict[key]:
                    if now_data_dict[key] != last_data_dict[key]:
                        print(now_data_dict[key], last_data_dict[key])
                    else:
                        pass
            last_data_dict = now_data_dict
            print(last_data_dict)
            time.sleep(1)

    def displacement_alarm_storage(self):
        pass


if __name__ == '__main__':
    alarm = Alarm().start()
