use tianyi;
create table `dec`(
datetime date,
productname varchar(50),
deliverymonth varchar(50),
openprice int,
highestprice int,
lowestprice int,
closeprice int,
presettlementprice int,
settlementprice int,
zd_chg int,
zd1_chg int,
volume int(18),
openinterest int(18),
openinterestchg int,
turnover decimal(18,2),
primary key(datetime,productname,deliverymonth)
)engine=INNODB default charset=utf8