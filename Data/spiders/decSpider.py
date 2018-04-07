# -*- coding: utf-8 -*-
import time
import scrapy
from Data.items import DataItem
import re
from Data.utils import select_update_time


class DecspiderSpider(scrapy.Spider):
    name = "decSpider"
    custom_settings = {'DOWNLOAD_DELAY':'0.2'}
    url = "http://www.dce.com.cn/publicweb/quotesdata/dayQuotesCh.html"
    today_time = time.time()

    def start_requests(self):
        """初始爬去时间为 2003-01-02 16:00:00 """
        start_time = select_update_time('dec') + 57600
        while start_time < self.today_time:
            start_time += 86400
            year = time.strftime('%Y', time.localtime(start_time))
            month = str(int(time.strftime('%m', time.localtime(start_time)).strip('0')) -1)
            day = time.strftime('%d', time.localtime(start_time))
            yield scrapy.FormRequest(self.url,formdata={"dayQuotes.variety": "all", "dayQuotes.trade_type": "0",
                                        "year" : year,"month" : month,"day" : day},callback=self.parse,meta={'time':start_time})

    def parse(self, response):
        """判断并解析获取数据"""
        trList = response.css('table tr')
        if trList:
            item = DataItem()
            for tr in trList[1:]:
                tdList = [td.strip() for td in tr.css('td::text').extract()]
                if tdList:
                    item['time'] = time.strftime('%Y-%m-%d', time.localtime(response.meta['time']))
                    item['productname'] = tdList[0]
                    judge = tdList[1]
                    if not judge:
                        item['deliverymonth'] = tdList[0][-2:]
                    else:
                        item['deliverymonth'] = judge
                    item['openprice'] = (None if len(tdList[2])<=1 else re.sub(r',','',tdList[2]))
                    item['highestprice'] = (None if len(tdList[3])<=1 else re.sub(r',','',tdList[3]))
                    item['lowestprice'] = (None if len(tdList[4])<=1 else re.sub(r',','',tdList[4]))
                    item['closeprice'] = (None if len(tdList[5])<=1 else re.sub(r',','',tdList[5]))
                    item['presettlementprice'] = (None if len(tdList[6])<=1 else re.sub(r',','',tdList[6]))
                    item['settlementprice'] = (None if len(tdList[7])<=1 else re.sub(r',','',tdList[7]))
                    item['zd1_chg'] = (re.sub(r',','',tdList[8]) if tdList[8] else None)
                    item['zd2_chg'] = (re.sub(r',','',tdList[9]) if tdList[9] else None)
                    item['volume'] = re.sub(r',','',tdList[10])
                    item['openinterest'] = re.sub(r',','',tdList[11])
                    item['openinterestchg'] = re.sub(r',','',tdList[12])
                    item['turnover'] = re.sub(r',','',tdList[13])
                    item['web_name'] = 'dec'
                    yield item


