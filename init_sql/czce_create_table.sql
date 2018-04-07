use tianyi;
create table czce(
datetime date,
productname varchar(50),
deliverymonth varchar(50),
presettlementprice decimal(18,2),
openprice decimal(18,2),
highestprice decimal(18,2),
lowestprice decimal(18,2),
closeprice decimal(18,2),
settlementprice decimal(18,2),
zd1_chg decimal(18,2),
zd2_chg decimal(18,2),
volume int(18),
openinterest int(18),
openinterestchg int(18),
turnover decimal(18,2),
deliveryprice decimal(18,2),
primary key(datetime,productname,deliverymonth)
)engine=INNODB default charset=utf8