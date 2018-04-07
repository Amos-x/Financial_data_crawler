CREATE TABLE `lingtong` (
  `ID_` int(18) NOT NULL AUTO_INCREMENT,
  `area` varchar(50) NOT NULL COMMENT '地区',
  `metal` varchar(50) NOT NULL COMMENT '金属类型',
  `pub_date` date NOT NULL,
  `name` varchar(255) NOT NULL COMMENT '金属细分的种类全名',
  `min_price` int(10) DEFAULT NULL COMMENT '最小价',
  `max_price` int(10) DEFAULT NULL COMMENT '最高价',
  `mid_price` int(10) DEFAULT NULL COMMENT '中间价',
  `rise_fall` int(10) DEFAULT NULL COMMENT '涨跌',
  `unit` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`ID_`),
  UNIQUE KEY `唯一性` (`area`,`metal`,`pub_date`,`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1000421903 DEFAULT CHARSET=utf8;

