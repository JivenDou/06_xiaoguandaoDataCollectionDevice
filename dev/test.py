"""
@File  :test.py
@Author:
@Date  :2021/7/19/001911:45:09
@Desc  :
"""
import redis


def set_value(data_dict):
    try:
        pipe = conn.pipeline(transaction=True)
        for key_name in data_dict.keys():
            pipe.set(key_name, data_dict[key_name], ex=600)  # redis过期时间10mines
        pipe.execute()
    except Exception as e:
        print(e)
        return e
    else:
        return True


def get_value(keys):
    dict = {}
    try:
        pipe = conn.pipeline(transaction=True)
        for index in range(len(keys)):
            pipe.get(keys[index])
        result = pipe.execute()
        for index in range(len(keys)):
            dict[keys[index]] = result[index]
        return dict
    except Exception as e:
        return e


if __name__ == '__main__':
    conn = redis.StrictRedis(host="127.0.0.1", port=6379, db=0, decode_responses=True)
    set_value(data_dict={"c1": 1})
    value = get_value(["c1", "c2", "c3"])
    print(value)
