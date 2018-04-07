use tianyi;
create table cffex(
datetime date,
productid varchar(50),
deliverymonth varchar(50),
openprice decimal(18,1),
highestprice decimal(18,1),
lowestprice decimal(18,1),
closeprice decimal(18,1),
presettlementprice decimal(18,1),
settlementprice decimal(18,1),
zd1_chg decimal(18,1),
zd2_chg decimal(18,1),
volume int,
turnover decimal(18,3),
openinterest decimal(18,1),
primary key(datetime,productid,deliverymonth)
)engine=INNODB default charset=utf8