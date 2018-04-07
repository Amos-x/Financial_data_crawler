# -*- coding: utf-8 -*-
import scrapy
import time
from Data.items import DataItem
import re
from Data.utils import select_update_time


class CzcespiderSpider(scrapy.Spider):
    name = 'czceSpider'
    url = 'http://www.czce.com.cn/cms/cmsface/czce/exchangefront/calendarnewquery.jsp'
    today_time = time.time()

    def start_requests(self):
        start_time = select_update_time('czce') +57600
        while start_time < self.today_time:
            start_time += 86400
            datetime = time.strftime('%Y-%m-%d',time.localtime(start_time))
            data = {"dataType": "DAILY",
                    "pubDate": datetime,
                    'commodity': '', }
            yield scrapy.FormRequest(self.url,formdata=data,meta={'time':datetime},callback=self.html_parse)

    def html_parse(self,response):
        tr_list = response.css('table#senfe.table tr')[1:-1]
        if tr_list:
            item = DataItem()
            type_name =''
            for tr in tr_list[1:]:
                td_list = [x.strip() for x in tr.css('td::text').extract()]
                item['time'] = response.meta['time']
                item['deliverymonth'] = td_list[0]
                if len(td_list[0]) == 4:
                    type_name = type_name
                    item['deliverymonth'] = type_name
                else:
                    type_name = td_list[0][:2]
                item['productname'] = type_name
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