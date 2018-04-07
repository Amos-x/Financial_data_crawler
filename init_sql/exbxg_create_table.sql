use tianyi;
create table exbxg(
datetime date,
productname varchar(50),
contactid varchar(50),
presettlementprice decimal(18,1),
openprice decimal(18,1),
highestprice decimal(18,1),
lowestprice decimal(18,1),
closeprice decimal(18,1),
averageprice decimal(18,1),
upanddown decimal(18,2),
volume int(18),
turnover int(18),
openinterest int(18),
openinterestchg int(18),
primary key(datetime,productname,contactid)
)engine=INNODB default charset=utf8;