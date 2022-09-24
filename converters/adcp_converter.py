"""
@Date  :2021/5/21/00219:10:57
@Desc  :
"""
from logging_config import logger
from converter import Converter


# data = b' 4 24 2021 12  9 59 0 32 11.7 1498.7 194.7 -2.2 0.6 1.008 12.58 0 0\r\n  1    331 2954\r\n  2    164 2448\r\n  3    171 1438\r\n  4    137 1034\r\n  5     38 2292\r\n  6    185 3027\r\n  7    162  928\r\n  8    611 3209\r\n  9    470 3287\r\n 10    463 3111\r\n 11    914 1178\r\n 12    149  390\r\n 13    703  939\r\n 14    411 2452\r\n 15    158 1111\r\n 16    206  710\r\n 17    673 1099\r\n 18    156  955\r\n 19    324  991\r\n 20    127  396\r\n 21    335 2590\r\n 22    105 3485\r\n 23    263 2615\r\n 24    179 1201\r\n 25    114 1496\r\n 26    669  844\r\n 27    105 2831\r\n 28    720 1256\r\n 29    449  839\r\n 30    392  818\r\n' 实收
# data = b' 4 24 2021 11 29 59 0 32 11.7 1498.7 194.9 -2.2 0.7 1.001 12.57 0 0\r\n  1    311 3003\r\n  2     91 1489\r\n  3     97 1476\r\n  4    100 1269\r\n  5     47  997\r\n  6     50 1074\r\n  7    158   40\r\n  8    487 3545\r\n  9    411 3268\r\n 10    715 2939\r\n 11    425  204\r\n 12    206 2557\r\n 13    259  820\r\n 14    407 2153\r\n 15    237 1405\r\n 16    378  768\r\n 17    481 1191\r\n 18    856 3105\r\n 19    681  999\r\n 20    274  400\r\n 21    369 2852\r\n 22    332  208\r\n 23     48  366\r\n 24    497  539\r\n 25    770 1103\r\n 26    102 1750\r\n 27    514  659\r\n 28    180 1787\r\n 29    499  938\r\n 30    611 3350\r\n' 模拟收
#        b' 4 25 2021 3 26 59 0 32 11.7 1500.7 195.0 -2.2 0.7 1.025 13.19 0 0\r\n  1    124 1973\r\n  2    108 1211\r\n  3    393  982\r\n  4    182  159\r\n  5     75 3440\r\n  6    176 2566\r\n  7    268 2553\r\n  8    250 2333\r\n  9    282 2215\r\n 10    564 1113\r\n 11    505  974\r\n 12    285  940\r\n 13    329 1381\r\n 14    118 1087\r\n 15    276 1313\r\n 16    707 2832\r\n 17    385 1000\r\n 18    365 2530\r\n 19    514 1374\r\n 20    591  683\r\n 21   1109  837\r\n 22    889  955\r\n 23    333  829\r\n 24    194  515\r\n 25    466  786\r\n 26    243  445\r\n 27    107 1693\r\n 28    261  317\r\n 29    704 1008\r\n 30    301  219\r\n'
class AdcpConverter(Converter):
    def convert(self, config, data):
        if data:
            # logger.debug(config)
            logger.info(f"(ADCP)原始接收数据：{data}")
            dict = {}
            try:
                raw_data = data.decode().split("\r\n")
                logger.debug(f"(ADCP)解码分割：{raw_data}")
                if len(raw_data) == 32:
                    # logger.debug(raw_data)
                    raw_data = raw_data[1:-1]
                    flow_rate_data = []
                    flow_direction = []
                    for i in range(0, len(raw_data)):
                        t = raw_data[i].split(' ')  # 按空格分拆字符串得到字符串列表：['', '', '1', '', '', '', '211', '3075']
                        t = list(filter(None, t))  # 去除字符串列表中的空格：['1', '211', '3075']
                        t1 = [int(x) for x in t]  # 字符串列表转int列表：[1, 211, 3075]
                        flow_rate_data.append(t1[1] / 1000)  # 流速值除以1000
                        flow_direction.append(t1[2] / 10)  # 流向值除以10
                    format_data = flow_rate_data + flow_direction
                    logger.debug(f"(ADCP)解析后数据: {len(format_data)}, {format_data}")
                    j = 0
                    for index in config:
                        name = 'c' + str(index['serial_number'])
                        if index['divisor'] is not None:
                            format_data[j] = format_data[j] / index['divisor']
                        if index['offset'] is not None:
                            format_data[j] = format_data[j] - index['offset']
                        dict[name] = format_data[j]
                        j += 1
                    return dict
                elif len(raw_data) > 0:
                    return "pass"
                else:
                    return "error"
            except Exception as e:
                logger.error(e)
                return "error"
