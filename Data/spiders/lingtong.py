# -*- coding: utf-8 -*-
import scrapy
from Data.items import LingtongItem
import re
import time

class LingtongSpider(scrapy.Spider):
    name = 'lingtong'
    handle_httpstatus_list = [500]
    url = 'http://lingtong.info/gb/price.asp'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'Data.middlewares.LonglongLoginMiddleware': 1}
    }
    today_time = time.time()
    START_DATE = '2007-01-01'

    def start_requests(self):
        yield scrapy.Request(self.url,callback=self.next_parse,dont_filter=True)

    def next_parse(self,response):
        all_data = response.css('div.part1 div.fl.style05 div.content div.list')
        for classify in all_data:
            for metal in classify.css('a'):
                area = classify.css('span::text').extract_first()
                metal_type = metal.css('::text').extract_first()
                classroot = re.findall(r'classroot=(.*?)&',metal.css('::attr(href)').extract_first())[0]
                start_time = time.mktime(time.strptime(self.START_DATE,'%Y-%m-%d'))
                while start_time < self.today_time:
                    weekday = time.localtime(start_time).tm_wday
                    if weekday < 5:
                        check_time = time.strftime('%Y-%m-%d',time.localtime(start_time))
                        check_url = 'http://www.lingtong.info/gb/price.asp?classroot=%s&datew=%s' %(classroot,check_time)
                        yield scrapy.Request(check_url,callback=self.page_parse,meta={'area':area,'metal_type':metal_type,'date':check_time})
                    start_time += 86400

    def page_parse(self,response):
        res = response.css('div.page span::text').extract()
        if res:
            pages = re.findall(r'/共(.*?)页',res[5])[0]
            for page in range(1,int(pages)+1):
                check_url = response.url + '&page=' + str(page)
                yield scrapy.Request(check_url,callback=self.content_parse,meta={'area':response.meta['area'],'metal_type':response.meta['metal_type'],'date':response.meta['date']})

    def content_parse(self,response):
        metal_list = response.css('div.part3 table tr')
        for metal in metal_list:
            if metal.css('td').extract():
                item = LingtongItem()
                item['web_name'] = 'lingtong'
                item['area'] = response.meta['area']
                item['metal'] = response.meta['metal_type']
                item['date'] = response.meta['date']
                item['name'] = metal.css('td.name a::text').extract_first().strip()
                try:
                    str_price = metal.css('td.num::text').extract_first().strip()
                    price = metal.css('td.num::text').extract_first().strip().split('-')
                except:
                    price =[str_price,str_price]
                item['min_price'] = int(price[0])
                item['max_price'] = int(price[1])
                item['mid_price'] = metal.css('td')[2].css('::text').extract_first().strip()
                price = metal.css('span::text').extract_first()
                if price:
                    rise_or_fall = metal.css('span::attr(class)').extract_first()
                    if rise_or_fall == 'up':
                        item['rise_fall'] = '+' + price.strip()
                    if rise_or_fall == 'down':
                        item['rise_fall'] = '-' + price.strip()
                else:
                    item['rise_fall'] = None
                yield item

