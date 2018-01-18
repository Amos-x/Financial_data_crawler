# -*- coding: utf-8 -*-
import scrapy
import datetime
from Data.items import CnalItem
import json


class CnalSpider(scrapy.Spider):
    name = 'cnal'
    is_history = False

    def start_requests(self):
        self.today = datetime.datetime.today()
        if self.is_history:
            url = 'https://market.cnal.com/historical/search.html'
            start_time = self.today - datetime.timedelta(days=30)
            yield scrapy.FormRequest(url,callback=self.parse,dont_filter=True,formdata={
                'starttime': start_time.strftime('%Y-%m-%d'),
                'endtime': self.today.strftime('%Y-%m-%d'),
                'selectid': '25',
            })
        else:
            url = 'https://market.cnal.com/api/php/index.php?m=market&a=GetNewJson'
            yield scrapy.Request(url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        if self.is_history:
            tr_list = response.css('div.content table tr')[1:-1]
            for tr in tr_list:
                item = CnalItem()
                groups = tr.css('td::text').extract()
                item['web_name'] = 'cnal'
                item['name'] = groups[0]
                item['min_price'] = groups[1]
                item['max_price'] = groups[2]
                item['aver_price'] = groups[3]
                item['rise_fall'] = groups[4]
                item['date'] = groups[5]
                yield item

        else:
            result = json.loads(response.text)['spot']['25']
            item = CnalItem()
            item['web_name'] = 'cnal'
            item['name'] = 'A00铝'
            item['min_price'] = result.get('min')
            item['max_price'] = result.get('max')
            item['aver_price'] = result.get('average')
            item['rise_fall'] = result.get('move')
            item['date'] = self.today.strftime('%Y-%m-%d')
            yield item
