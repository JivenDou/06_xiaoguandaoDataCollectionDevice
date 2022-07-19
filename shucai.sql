-- Adminer 4.8.0 MySQL 5.7.26 dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

CREATE DATABASE `shucai` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `shucai`;

DROP TABLE IF EXISTS `command`;
CREATE TABLE `command` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `station_name` varchar(30) NOT NULL,
  `command` json NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `data_point_tbl`;
CREATE TABLE `data_point_tbl` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `station_name` varchar(120) DEFAULT NULL COMMENT '站点名称',
  `serial_number` int(11) DEFAULT NULL COMMENT '序列号',
  `device_id` varchar(20) DEFAULT NULL COMMENT '设备ID',
  `device_name` varchar(120) DEFAULT NULL COMMENT '设备名称',
  `io_point_name` varchar(120) DEFAULT NULL COMMENT 'IO点名称',
  `unit` varchar(120) DEFAULT NULL COMMENT '单位',
  `address` varchar(20) DEFAULT NULL COMMENT '地址',
  `data_type` varchar(20) DEFAULT NULL COMMENT '数据类型',
  `offset` float DEFAULT NULL COMMENT '偏移量',
  `divisor` float DEFAULT NULL COMMENT '除数',
  `decimal` int(11) DEFAULT NULL COMMENT '保留小数的位数',
  `storage_type` varchar(20) DEFAULT NULL COMMENT '存储类型',
  `low_limit` float DEFAULT NULL COMMENT '下限',
  `up_limit` float DEFAULT NULL COMMENT '上限',
  `alarm_low_limit` float DEFAULT NULL COMMENT '越下报警限',
  `alarm_up_limit` float DEFAULT NULL COMMENT '越上报警限',
  `negation` tinyint(4) DEFAULT NULL COMMENT '取反',
  `signal_type` enum('Switch','Analog') DEFAULT NULL COMMENT '开关量、模拟量',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `data_point_tbl` (`id`, `station_name`, `serial_number`, `device_id`, `device_name`, `io_point_name`, `unit`, `address`, `data_type`, `offset`, `divisor`, `decimal`, `storage_type`, `low_limit`, `up_limit`, `alarm_low_limit`, `alarm_up_limit`, `negation`, `signal_type`) VALUES
(1,	'wxt536',	1,	'1',	'wxt536',	'风向',	'°',	'1',	NULL,	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(2,	'wxt536',	2,	'1',	'wxt536',	'风速',	'm/s',	'2',	NULL,	NULL,	NULL,	2,	'float',	0,	60,	0,	30,	NULL,	'Analog'),
(3,	'wxt536',	3,	'1',	'wxt536',	'气温',	'°C',	'3',	NULL,	NULL,	NULL,	2,	'float',	-30,	50,	0,	36,	NULL,	'Analog'),
(4,	'wxt536',	4,	'1',	'wxt536',	'相对湿度',	'%RH',	'4',	NULL,	NULL,	NULL,	2,	'float',	0,	100,	0,	1000,	NULL,	'Analog'),
(5,	'wxt536',	5,	'1',	'wxt536',	'气压',	'hPa',	'5',	NULL,	NULL,	NULL,	2,	'float',	600,	1300,	600,	1300,	NULL,	'Analog'),
(6,	'wxt536',	6,	'1',	'wxt536',	'日降雨量',	'mm',	'6',	NULL,	NULL,	NULL,	2,	'float',	0,	1000,	0,	1000,	NULL,	'Analog'),
(7,	'td266',	7,	'1',	'td266',	'流速',	'm/s',	'2',	NULL,	NULL,	100,	2,	'float',	0,	10,	0,	300,	NULL,	'Analog'),
(8,	'td266',	8,	'1',	'td266',	'流向',	'Deg.M',	'3',	NULL,	NULL,	NULL,	2,	'float',	0,	360,	0,	360,	NULL,	'Analog'),
(9,	'td266',	9,	'1',	'td266',	'艏向',	'Deg.M',	'6',	NULL,	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(10,	'td266',	10,	'1',	'td266',	'X轴姿态',	'Deg',	'7',	NULL,	NULL,	NULL,	2,	'float',	-45,	45,	NULL,	NULL,	NULL,	'Analog'),
(11,	'td266',	11,	'1',	'td266',	'Y轴姿态',	'Deg',	'8',	NULL,	NULL,	NULL,	2,	'float',	-45,	45,	NULL,	NULL,	NULL,	'Analog'),
(12,	'shuizhi',	12,	'1',	'shuizhi',	'溶解氧',	'mg/L',	'',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(13,	'shuizhi',	13,	'1',	'shuizhi',	'温度',	'°C',	'',	'',	NULL,	NULL,	2,	'float',	-5,	40,	-5,	40,	NULL,	'Analog'),
(14,	'shuizhi',	14,	'1',	'shuizhi',	'盐度',	'PSU',	'',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(15,	'shuizhi',	15,	'1',	'shuizhi',	'PH',	'',	'',	'',	NULL,	NULL,	2,	'float',	0,	14,	0,	14,	NULL,	'Analog'),
(16,	'shuizhi',	16,	'1',	'shuizhi',	'叶绿素',	'μg/L',	'',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(17,	'shuizhi',	17,	'1',	'shuizhi',	'深度',	'm',	'',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(18,	'adcp',	18,	'1',	'adcp',	'1m流速',	'm/s',	'1',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(19,	'adcp',	19,	'1',	'adcp',	'2m流速',	'm/s',	'2',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(20,	'adcp',	20,	'1',	'adcp',	'3m流速',	'm/s',	'3',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(21,	'adcp',	21,	'1',	'adcp',	'4m流速',	'm/s',	'4',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(22,	'adcp',	22,	'1',	'adcp',	'5m流速',	'm/s',	'5',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(23,	'adcp',	23,	'1',	'adcp',	'6m流速',	'm/s',	'6',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(24,	'adcp',	24,	'1',	'adcp',	'7m流速',	'm/s',	'7',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(25,	'adcp',	25,	'1',	'adcp',	'8m流速',	'm/s',	'8',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(26,	'adcp',	26,	'1',	'adcp',	'9m流速',	'm/s',	'9',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(27,	'adcp',	27,	'1',	'adcp',	'10m流速',	'm/s',	'10',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(28,	'adcp',	28,	'1',	'adcp',	'11m流速',	'm/s',	'11',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(29,	'adcp',	29,	'1',	'adcp',	'12m流速',	'm/s',	'12',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(30,	'adcp',	30,	'1',	'adcp',	'13m流速',	'm/s',	'13',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(31,	'adcp',	31,	'1',	'adcp',	'14m流速',	'm/s',	'14',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(32,	'adcp',	32,	'1',	'adcp',	'15m流速',	'm/s',	'15',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(33,	'adcp',	33,	'1',	'adcp',	'16m流速',	'm/s',	'16',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(34,	'adcp',	34,	'1',	'adcp',	'17m流速',	'm/s',	'17',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(35,	'adcp',	35,	'1',	'adcp',	'18m流速',	'm/s',	'18',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(36,	'adcp',	36,	'1',	'adcp',	'19m流速',	'm/s',	'19',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(37,	'adcp',	37,	'1',	'adcp',	'20m流速',	'm/s',	'20',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(38,	'adcp',	38,	'1',	'adcp',	'21m流速',	'm/s',	'21',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(39,	'adcp',	39,	'1',	'adcp',	'22m流速',	'm/s',	'22',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(40,	'adcp',	40,	'1',	'adcp',	'23m流速',	'm/s',	'23',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(41,	'adcp',	41,	'1',	'adcp',	'24m流速',	'm/s',	'24',	NULL,	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(42,	'adcp',	42,	'1',	'adcp',	'25m流速',	'm/s',	'25',	'',	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(43,	'adcp',	43,	'1',	'adcp',	'26m流速',	'm/s',	'26',	'',	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(44,	'adcp',	44,	'1',	'adcp',	'27m流速',	'm/s',	'27',	'',	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(45,	'adcp',	45,	'1',	'adcp',	'28m流速',	'm/s',	'28',	'',	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(46,	'adcp',	46,	'1',	'adcp',	'29m流速',	'm/s',	'29',	'',	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(47,	'adcp',	47,	'1',	'adcp',	'30m流速',	'm/s',	'30',	'',	NULL,	NULL,	2,	'float',	0,	5,	NULL,	NULL,	NULL,	'Analog'),
(48,	'adcp',	48,	'1',	'adcp',	'1m流向',	'°',	'31',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(49,	'adcp',	49,	'1',	'adcp',	'2m流向',	'°',	'32',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(50,	'adcp',	50,	'1',	'adcp',	'3m流向',	'°',	'33',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(51,	'adcp',	51,	'1',	'adcp',	'4m流向',	'°',	'34',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(52,	'adcp',	52,	'1',	'adcp',	'5m流向',	'°',	'35',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(53,	'adcp',	53,	'1',	'adcp',	'6m流向',	'°',	'36',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(54,	'adcp',	54,	'1',	'adcp',	'7m流向',	'°',	'37',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(55,	'adcp',	55,	'1',	'adcp',	'8m流向',	'°',	'38',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(56,	'adcp',	56,	'1',	'adcp',	'9m流向',	'°',	'39',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(57,	'adcp',	57,	'1',	'adcp',	'10流向',	'°',	'40',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(58,	'adcp',	58,	'1',	'adcp',	'11流向',	'°',	'41',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(59,	'adcp',	59,	'1',	'adcp',	'12流向',	'°',	'42',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(60,	'adcp',	60,	'1',	'adcp',	'13流向',	'°',	'43',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(61,	'adcp',	61,	'1',	'adcp',	'14流向',	'°',	'44',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(62,	'adcp',	62,	'1',	'adcp',	'15流向',	'°',	'45',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(63,	'adcp',	63,	'1',	'adcp',	'16流向',	'°',	'46',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(64,	'adcp',	64,	'1',	'adcp',	'17流向',	'°',	'47',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(65,	'adcp',	65,	'1',	'adcp',	'18流向',	'°',	'48',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(66,	'adcp',	66,	'1',	'adcp',	'19流向',	'°',	'49',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(67,	'adcp',	67,	'1',	'adcp',	'20流向',	'°',	'50',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(68,	'adcp',	68,	'1',	'adcp',	'21流向',	'°',	'51',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(69,	'adcp',	69,	'1',	'adcp',	'22流向',	'°',	'52',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(70,	'adcp',	70,	'1',	'adcp',	'23流向',	'°',	'53',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(71,	'adcp',	71,	'1',	'adcp',	'24流向',	'°',	'54',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(72,	'adcp',	72,	'1',	'adcp',	'25流向',	'°',	'55',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(73,	'adcp',	73,	'1',	'adcp',	'26流向',	'°',	'56',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(74,	'adcp',	74,	'1',	'adcp',	'27流向',	'°',	'57',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(75,	'adcp',	75,	'1',	'adcp',	'28流向',	'°',	'58',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(76,	'adcp',	76,	'1',	'adcp',	'29流向',	'°',	'59',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(77,	'adcp',	77,	'1',	'adcp',	'30流向',	'°',	'60',	'',	NULL,	NULL,	2,	'float',	0,	360,	NULL,	NULL,	NULL,	'Analog'),
(78,	'sm140',	78,	'1',	'sm140',	'有效波高',	'm',	'8',	'',	NULL,	NULL,	2,	'float',	0,	50,	0,	50,	NULL,	'Analog'),
(79,	'sm140',	79,	'1',	'sm140',	'最大波高',	'm',	'10',	'',	NULL,	NULL,	2,	'float',	0,	50,	0,	50,	NULL,	'Analog'),
(81,	'sm140',	81,	'1',	'sm140',	'有效波周期',	's',	'20',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(82,	'sm140',	82,	'1',	'sm140',	'平均波周期',	's',	'28',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(83,	'sm140',	83,	'1',	'sm140',	'最大波周期',	's',	'30',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog'),
(84,	'sm140',	84,	'1',	'sm140',	'最大波高的波周期',	's',	'32',	'',	NULL,	NULL,	2,	'float',	0,	100,	0,	100,	NULL,	'Analog');

DROP TABLE IF EXISTS `shuizhi_insitu_instruct`;
CREATE TABLE `shuizhi_insitu_instruct` (
  `parameter_id` int(6) NOT NULL COMMENT 'id，用于判断是哪个参数',
  `name` varchar(10) CHARACTER SET utf8 NOT NULL COMMENT '参数名称',
  `units_id` int(6) DEFAULT NULL COMMENT '单位id，判断单位值',
  `station_code` varchar(8) CHARACTER SET utf8 NOT NULL COMMENT '站号',
  `function_code` varchar(8) CHARACTER SET utf8 NOT NULL COMMENT '功能码',
  `address` int(6) NOT NULL COMMENT '寄存器的位置'
) ENGINE=InnoDB DEFAULT CHARSET=utf16 COMMENT='读取水质参数，组合In-situ发送指令';

INSERT INTO `shuizhi_insitu_instruct` (`parameter_id`, `name`, `units_id`, `station_code`, `function_code`, `address`) VALUES
(3,	'深度',	NULL,	'01',	'03',	5464),
(12,	'盐度',	NULL,	'01',	'03',	5527),
(17,	'PH',	NULL,	'01',	'03',	5562),
(51,	'叶绿素',	NULL,	'01',	'03',	5800),
(1,	'温度',	NULL,	'01',	'03',	5450),
(20,	'溶解氧',	NULL,	'01',	'03',	5583);

DROP TABLE IF EXISTS `station_info_tbl`;
CREATE TABLE `station_info_tbl` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `station_name` varchar(120) NOT NULL,
  `connector_module` varchar(120) NOT NULL,
  `connector` varchar(120) NOT NULL,
  `connector_config` json NOT NULL,
  `converter_module` varchar(120) NOT NULL,
  `converter` varchar(120) NOT NULL,
  `status` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO `station_info_tbl` (`id`, `station_name`, `connector_module`, `connector`, `connector_config`, `converter_module`, `converter`, `status`) VALUES
(1,	'wxt536',	'tcp_connector',	'TcpConnector',	'{\"ip\": \"192.168.1.84\", \"port\": 4001, \"save_frequency\": 5, \"alarm_save_frequency\": 15}',	'wxt536_converter',	'WXT536Converter',	1),
(2,	'sm140',	'tcp_connector',	'TcpConnector',	'{\"ip\": \"192.168.1.83\", \"port\": 4001, \"save_frequency\": 5, \"alarm_save_frequency\": 15}',	'nmea0183_converter',	'NEMA0183Converter',	1),
(3,	'td266',	'tcp_connector',	'TcpConnector',	'{\"ip\": \"192.168.1.89\", \"port\": 4001, \"save_frequency\": 180, \"alarm_save_frequency\": 15}',	'td266_converter',	'TD266Converter',	1),
(4,	'adcp',	'tcp_connector',	'TcpConnector',	'{\"ip\": \"192.168.1.252\", \"port\": 4001, \"save_frequency\": 180, \"alarm_save_frequency\": 15}',	'adcp_converter',	'AdcpConverter',	1),
(5,	'shuizhi',	'shuizhi_tcp_connector',	'ShuizhiTcpConnector',	'{\"ip\": \"192.168.1.254\", \"port\": 4001, \"save_frequency\": 5, \"alarm_save_frequency\": 15}',	'shuizhi_converter',	'ShuizhiConverter',	1);

-- 2022-07-19 03:10:34
