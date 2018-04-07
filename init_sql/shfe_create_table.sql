use tianyi;
create table shfe(
datetime date,
productname varchar(50),
deliverymonth varchar(50),
presettlementprice int,
openprice int,
highestprice int,
lowestprice int,
closeprice int,
settlementprice int,
zd1_chg int,
zd2_chg int,
volume int,
openinterest int,
openinterestchg int,
primary key(datetime,productname,deliverymonth))engine=INNODB default charset=utf8;
