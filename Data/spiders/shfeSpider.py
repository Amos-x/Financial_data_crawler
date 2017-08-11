# -*- coding: utf-8 -*-
import scrapy
import json
import time
try:
    from Data.settings import START_DATE
except:
    START_DATE = None
from Data.items import DataItem


class ShfeSpider(scrapy.Spider):
    name = 'shfeSpider'
    allowed_domains = ['www.shfe.com.cn']
    handle_httpstatus_list = [404]
    url = 'http://www.shfe.com.cn/data/dailydata/kx/kx{date}.dat'
    today_time = time.time()

    def start_requests(self):
        """初始时间为：2002-01-07 16：00：00 """
        if START_DATE:
            start_time = time.mktime(time.strptime(START_DATE,'%Y-%m-%d')) + 57600
        else:
            start_time = 1010332800.0 + 57600
        while start_time < self.today_time:
            yield scrapy.Request(self.url.format(date=time.strftime('%Y%m%d',time.localtime(start_time))),
                                 callback=self.parse,meta={'time':start_time})
            start_time += 86400


    def parse(self, response):
        """判断当天是否有数据 并解析提取数据"""
        if response.status == 404:
            return
        item = DataItem()
        results_list = json.loads(response.text)['o_curinstrument']
        for group in results_list:
            item['time'] = time.strftime('%Y-%m-%d',time.localtime(response.meta['time']))
            item['productname'] = group['PRODUCTNAME'].strip()
            item['deliverymonth'] = group['DELIVERYMONTH']
            item['openprice'] = (None if not group['OPENPRICE'] else group['OPENPRICE'])
            item['highestprice'] = (None if not group['HIGHESTPRICE'] else group['HIGHESTPRICE'])
            item['lowestprice'] = (None if not group['LOWESTPRICE'] else group['LOWESTPRICE'])
            item['closeprice'] = (None if not group['CLOSEPRICE'] else group['CLOSEPRICE'])
            item['presettlementprice'] = (None if not group['PRESETTLEMENTPRICE'] else group['PRESETTLEMENTPRICE'])
            item['settlementprice'] = (None if not group['SETTLEMENTPRICE'] else group['SETTLEMENTPRICE'])
            item['zd1_chg'] = (None if not group['ZD1_CHG'] else group['ZD1_CHG'])
            item['zd2_chg'] = (None if not group['ZD2_CHG'] else group['ZD2_CHG'])
            item['volume'] = (None if not group['VOLUME'] else group['VOLUME'])
            item['openinterest'] = (None if not group['OPENINTEREST'] else group['OPENINTEREST'])
            item['openinterestchg'] = (None if not group['OPENINTERESTCHG'] else group['OPENINTERESTCHG'])
            item['web_name'] = 'shfe'
            yield item



