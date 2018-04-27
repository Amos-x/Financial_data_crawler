# -*- coding: utf-8 -*-
import scrapy
from Data.items import CnalItem
import datetime


class SmmSpider(scrapy.Spider):
    name = 'smm'
    url = 'https://www.smm.cn/'

    def start_requests(self):
        yield scrapy.Request(self.url,callback=self.parse,dont_filter=True)

    def parse(self, response):
        tr_list = response.css('div.content-left-first-pirce tbody tr')
        for tr in tr_list:
            result = [x.strip() for x in tr.css('td ::text').extract()]
            if result[0] == 'SMM 1#电解铜' or result[0] == 'SMM 0#锌锭':
                item = CnalItem()
                item['web_name'] = 'cnal'
                item['name'] = result[0][4:]
                maxandmix = result[2].split('-')
                item['min_price'] = maxandmix[0]
                item['max_price'] = maxandmix[1]
                item['aver_price'] = result[3]
                item['rise_fall'] = result[4]
                toyear = datetime.datetime.today().year
                item['date'] = '%s-%s' %(toyear,result[5])
                yield item
