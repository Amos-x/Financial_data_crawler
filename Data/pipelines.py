# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import time

class Save_to_mysql(object):

    def __init__(self,host,port,username,passwd,db_name):
        self.host = host
        self.port = port
        self.username = username
        self.passwd = passwd
        self.db_name = db_name

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host = crawler.settings.get('MYSQL_HOST'),
            port = crawler.settings.get('MYSQL_PORT'),
            username = crawler.settings.get('MYSQL_USERNAME'),
            passwd = crawler.settings.get('MYSQL_PASSWORD'),
            db_name = crawler.settings.get('MYSQL_DB_NAME')
        )

    def open_spider(self,spider):
        self.client = pymysql.connect(host=self.host,port=self.port,user=self.username,passwd=self.passwd,db=self.db_name,charset='utf8')
        self.cursor = self.client.cursor()
        self.error = 0

    def close_spider(self,spider):
        self.client.close()
        print('插入数据库错误数：',self.error)

    def process_item(self,item,spider):
        if item['web_name'] == 'shfe':
            try:
                sql = "insert into shfe values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                self.cursor.execute(sql,(item['time'],item['productname'],item['deliverymonth'],item['presettlementprice'],
                                         item['openprice'],item['highestprice'],item['lowestprice'],item['closeprice'],
                                         item['settlementprice'],item['zd1_chg'],item['zd2_chg'],item['volume'],
                                         item['openinterest'],item['openinterestchg']))
                self.client.commit()
            except:
                self.error +=1

        if item['web_name'] == 'sge':
            try:
                sql = 'insert into sge values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(sql,(item['time'],item['productname'],item['openprice'],item['highestprice'],
                                         item['lowestprice'],item['closeprice'],item['zd1_chg'],item['zd2_chg'],
                                         item['averageprice'],item['volume'],item['turnover'],item['openinterest'],
                                         item['deliverypoint'],item['deliverynum']))
                self.client.commit()
            except:
                self.error +=1

        if item['web_name'] == 'exbxg':
            try:
                sql = 'insert into exbxg values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(sql,(item['time'],item['productname'],item['deliverymonth'],item['presettlementprice'],
                                         item['openprice'],item['highestprice'],item['lowestprice'],item['closeprice'],
                                         item['averageprice'],item['zd1_chg'],item['volume'],item['turnover'],
                                         item['openinterest'],item['openinterestchg']))
                self.client.commit()
            except:
                self.error += 1

        if item['web_name'] == 'dec':
            try:
                sql = 'insert into `dec` values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(sql,(item['time'],item['productname'],item['deliverymonth'],item['openprice'],
                                         item['highestprice'],item['lowestprice'],item['closeprice'],item['presettlementprice'],
                                         item['settlementprice'],item['zd1_chg'],item['zd2_chg'],item['volume'],
                                         item['openinterest'],item['openinterestchg'],item['turnover']))
                self.client.commit()
            except:
                self.error += 1

        if item['web_name'] == 'cffex':
            try:
                sql = 'insert into cffex values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(sql,(item['time'],item['productname'],item['deliverymonth'],item['openprice'],
                                         item['highestprice'],item['lowestprice'],item['closeprice'],item['presettlementprice'],
                                         item['settlementprice'],item['zd1_chg'],item['zd2_chg'],item['volume'],
                                         item['turnover'],item['openinterest']))
                self.client.commit()
            except:
                self.error += 1

        if item['web_name'] == 'czce':
            try:
                sql = 'insert into czce values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
                self.cursor.execute(sql,(item['time'],item['productname'],item['deliverymonth'],item['presettlementprice'],
                                         item['openprice'],item['highestprice'],item['lowestprice'],item['closeprice'],
                                         item['settlementprice'],item['zd1_chg'],item['zd2_chg'],item['volume'],
                                         item['openinterest'],item['openinterestchg'],item['turnover'],item['deliveryprice']))
                self.client.commit()
            except:
                self.error += 1

        if item['web_name'] == 'lingtong':
            sql = 'insert into lingtong(area,metal,pub_date,name,min_price,max_price,mid_price,rise_fall,unit) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,(item['area'],item['metal'],item['date'],item['name'],item['min_price'],
                                 item['max_price'],item['mid_price'],item['rise_fall'],item['unit']))
            self.client.commit()

        if item['web_name'] == 'ccmn':
            sql = 'insert into ccmn(pub_date,name,min_price,max_price,aver_price,rise_fall,unit) values(%s,%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,(item['date'],item['name'],item['min_price'],item['max_price'],
                                     item['aver_price'],item['rise_fall'],item['unit']))
            self.client.commit()

        if item['web_name'] == 'cnal':
            sql = 'insert into cnal(pub_date,name,min_price,max_price,aver_price,rise_fall) values(%s,%s,%s,%s,%s,%s)'
            self.cursor.execute(sql,(item['date'],item['name'],item['min_price'],item['max_price'],
                                     item['aver_price'],item['rise_fall']))
            self.client.commit()

        return item
