# -*- coding: utf-8 -*-
import scrapy
from Data.items import ChangjiangXHItem
import datetime


class CcmnSpider(scrapy.Spider):
    name = 'ccmn'
    year = datetime.datetime.today().year

    def start_requests(self):
        url = 'http://www.ccmn.cn/historyprice/cjxh_1/'
        yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'proxy':'http://119.145.165.118:8888'})

    def parse(self, response):
        result = response.css('div#list_elem table tr')[1:]
        if result:
            for group in result:
                item = ChangjiangXHItem()
                items = [x.strip() for x in group.css('td ::text').extract() if x.strip()]
                item['web_name'] = 'ccmn'
                item['date'] = '%s-%s' %(self.year,items[6])
                item['name'] = items[1]
                item['aver_price'] = items[3]
                item['rise_fall'] = items[4]
                item['unit'] = items[5]
                item['min_price'],item['max_price'] = items[2].split('—')
                yield item
