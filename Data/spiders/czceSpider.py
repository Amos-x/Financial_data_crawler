# -*- coding: utf-8 -*-
import scrapy
import time
from bs4 import BeautifulSoup
from Data.items import DataItem
import re

class CzcespiderSpider(scrapy.Spider):
    name = 'czceSpider'
    # allowed_domains = ['www.czce.com.cn']
    # start_urls = ['http://www.czce.com.cn/portal/jysj/qhjysj/mrhq/A09112001index_1.htm']
    url = 'http://www.czce.com.cn/portal/jysj/qhjysj/mrhq/A09112001index_1.htm/'
    today_time = time.time()
    custom_settings = {'DOWNLOADER_MIDDLEWARES': {'Data.middlewares.SeleniumMiddleware': 1}}

    def start_requests(self):
        start_time = 1388678400.0 + 57600  #1072886400.0 + 57600
        while start_time < self.today_time:
            datetime = time.strftime('%Y-%m-%d',time.localtime(start_time))
            yield scrapy.Request(self.url+datetime,meta={'time':datetime},callback=self.html_parse)
            start_time += 86400

    def html_parse(self,response):
        soup = BeautifulSoup(response.text,'lxml')
        tr_list = soup.select('table')[-1].select('tr')
        if len(tr_list)>1:
            item = DataItem()
            type_name =''
            for tr in tr_list[1:]:
                td_list = [td.get_text().strip() for td in tr.select('td')]
                item['time'] = response.url
                type_name = (type_name if len(td_list[0])==2 else td_list[0][:2])
                item['productname'] = type_name
                item['deliverymonth'] = td_list[0]
                item['presettlementprice'] = (None if not td_list[1] else re.sub(r',','',td_list[1]))
                item['openprice'] = (None if not td_list[2] else re.sub(r',','',td_list[2]))
                item['highestprice'] = (None if not td_list[3] else re.sub(r',','',td_list[3]))
                item['lowestprice'] = (None if not td_list[4] else re.sub(r',','',td_list[4]))
                item['closeprice'] = (None if not td_list[5] else re.sub(r',','',td_list[5]))
                item['settlementprice'] = (None if not td_list[6] else re.sub(r',','',td_list[6]))
                if len(td_list) ==13:
                    a = 0
                    item['zd1_chg'] = None
                    item['zd2_chg'] = (None if not td_list[7] else re.sub(r',','',td_list[7]))
                if len(td_list) ==14:
                    a = 1
                    item['zd1_chg'] = (None if not td_list[7] else re.sub(r',','',td_list[7]))
                    item['zd2_chg'] = (None if not td_list[8] else re.sub(r',','',td_list[8]))
                item['volume'] = (None if not td_list[8+a] else re.sub(r',','',td_list[8+a]))
                item['openinterest'] = (None if not td_list[9+a] else re.sub(r',','',td_list[9+a]))
                item['openinterestchg'] = (None if not td_list[10+a] else re.sub(r',','',td_list[10+a]))
                item['turnover'] = (None if not td_list[11+a] else re.sub(r',','',td_list[11+a]))
                item['deliveryprice'] = (None if not td_list[12+a] else re.sub(r',','',td_list[12+a]))
                item['web_name'] = 'czce'
                yield item
