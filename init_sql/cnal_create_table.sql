CREATE TABLE `cnal` (
  `ID_` int(18) NOT NULL AUTO_INCREMENT,
  `pub_date` date NOT NULL,
  `name` varchar(50) NOT NULL,
  `min_price` decimal(10,2) DEFAULT NULL,
  `max_price` decimal(10,2) DEFAULT NULL,
  `aver_price` decimal(10,2) DEFAULT NULL,
  `unit` varchar(255) DEFAULT NULL,
  `rise_fall` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`ID_`),
  UNIQUE KEY `唯一性` (`pub_date`,`name`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1000000058 DEFAULT CHARSET=utf8;

