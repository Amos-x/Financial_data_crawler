use tianyi;
create table sge(
datetime date,
productname varchar(50),
openprice decimal(18,2),
highestprice decimal(18,2),
lowestprice decimal(18,2),
closeprice decimal(18,2),
upanddown decimal(18,2),
chg decimal(18,2),
vwap decimal(18,2),
volume decimal(18,2),
turnover decimal(18,2),
openinterest int,
deliverypoint varchar(50),
deliverynum int,
primary key(datetime,productname)
)engine=INNODB default charset=utf8;