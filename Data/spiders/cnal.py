# -*- coding: utf-8 -*-
import scrapy
import datetime
import time
from Data.items import CnalItem
import json


class CnalSpider(scrapy.Spider):
    name = 'cnal'
    is_history = True

    def start_requests(self):
        yield scrapy.Request('https://market.cnal.com/share/market/sme30.json',callback=self.next_parse,dont_filter=True)
        yield scrapy.Request('https://market.cnal.com/share/market/nc30.json',callback=self.next_parse,dont_filter=True)

    def next_parse(self,response):
        selectid = False
        select_name = False
        for key,value in json.loads(response.text)['name'].items():
            if value == '铝':
                selectid = key
                select_name = '铝'
            if value == 'A00铝':
                selectid = key
                select_name = 'A00铝(南储)'
        if selectid:
            self.today = datetime.datetime.today()
            if self.is_history:
                url = 'https://market.cnal.com/historical/search.html'
                start_time = self.today - datetime.timedelta(days=30)
                yield scrapy.FormRequest(url,callback=self.parse,dont_filter=True,formdata={
                    'starttime': start_time.strftime('%Y-%m-%d'),
                    'endtime': self.today.strftime('%Y-%m-%d'),
                    'selectid': selectid,
                },meta={'selectid':selectid,'select_name':select_name})
            else:
                url = 'https://market.cnal.com/api/php/index.php?m=market&a=GetNewJson'
                yield scrapy.Request(url,callback=self.parse,dont_filter=True,meta={'selectid':selectid,'select_name':select_name})

    def parse(self, response):
        if self.is_history:
            tr_list = response.css('div.content table tr')[1:-1]
            for tr in tr_list:
                item = CnalItem()
                groups = tr.css('td::text').extract()
                item['web_name'] = 'cnal'
                item['name'] = response.meta['select_name']
                item['min_price'] = groups[1]
                item['max_price'] = groups[2]
                item['aver_price'] = groups[3]
                item['rise_fall'] = groups[4]
                item['date'] = groups[5]
                yield item
        else:
            result = json.loads(response.text)['spot'][response.meta['selectid']]
            item = CnalItem()
            item['web_name'] = 'cnal'
            item['name'] = response.meta['select_name']
            item['min_price'] = result.get('min')
            item['max_price'] = result.get('max')
            item['aver_price'] = result.get('average')
            item['rise_fall'] = result.get('move')
            item['date'] = time.strftime("%Y-%m-%d",time.localtime(int(result.get('createtime'))))
            yield item
