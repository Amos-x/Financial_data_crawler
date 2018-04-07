CREATE TABLE `new_exbxg` (
  `datetime` datetime NOT NULL COMMENT '日期',
  `lowNickelCostPrice` decimal(10,2) DEFAULT NULL COMMENT '低镍铁成本价格',
  `highNickelCostPrice` decimal(10,2) DEFAULT NULL COMMENT '高镍铁成本价格',
  `stainlessPrice` decimal(10,2) DEFAULT NULL COMMENT '无锡不锈钢指数价格',
  `lowNickelWuxiPrice` decimal(10,2) DEFAULT NULL COMMENT '低镍铁成本和无锡价差',
  `highNickelWuxiPrice` decimal(10,2) DEFAULT NULL COMMENT '高镍铁成本和无锡价差',
  PRIMARY KEY (`datetime`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;