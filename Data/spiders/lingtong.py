# -*- coding: utf-8 -*-
import scrapy
from Data.items import LingtongItem
import re
import time
import requests

class LingtongSpider(scrapy.Spider):
    name = 'lingtong'
    handle_httpstatus_list = [500]
    url = 'http://lingtong.info/gb/price.asp'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {'Data.middlewares.LonglongLoginMiddleware': 1}
    }
    today_time = time.time()
    START_DATE = '2018-02-05'
    is_history = False

    def start_requests(self):
        if self.is_history:
            start_time = time.mktime(time.strptime(self.START_DATE, '%Y-%m-%d'))
            while start_time < self.today_time:
                weekday = time.localtime(start_time).tm_wday
                if weekday < 5:
                    check_time = time.strftime('%Y-%m-%d', time.localtime(start_time))
                    check_url = 'http://www.lingtong.info/gb/price.asp?datew=%s' %check_time
                    yield scrapy.Request(check_url,callback=self.next_parse,meta={'check_time':check_time})
                start_time = start_time + 86400
        else:
            today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
            yield scrapy.Request('http://www.lingtong.info/gb/price.asp?datew=%s' %today,callback=self.next_parse,
                                 meta={'check_time':today})

    def next_parse(self,response):
        if response.status != 200:
            response.request.dont_filter = True
            yield response.request
        else:
            url_list = response.css('div.part1 div.fl.style05 div.content div.list a::attr(href)').extract()
            url_text = ','.join(url_list)
            classroot_list = re.findall('classroot=(.*?)&',url_text)
            for classroot in list(set(classroot_list)):
                check_url = 'http://www.lingtong.info/gb/price.asp?classroot=%s&datew=%s' %(classroot,response.meta['check_time'])
                yield scrapy.Request(check_url,callback=self.content_parse)

    # def page_parse(self,response):
    #     res = response.css('div.page span::text').extract()
    #     if res:
    #         pages = re.findall(r'/共(.*?)页',res[5])[0]
    #         for page in range(1,int(pages)+1):
    #             check_url = response.url + '&page=' + str(page)
    #             yield scrapy.Request(check_url,callback=self.content_parse,meta={'area':response.meta['area'],'metal_type':response.meta['metal_type'],'date':response.meta['date']})

    def content_parse(self,response):
        if response.status != 200:
            response.request.dont_filter = True
            yield response.request
        else:
            metal_list = response.css('div.part3 table tr')
            if metal_list:
                title_content = response.css('div.part3 div.title div.fl ::text').extract()
                cont = [x.strip() for x in title_content if x.strip()]
                pub_time = cont[1]
                unit = cont[3]
                try:
                    metal_name,area = re.findall('^(.*?)（(.*?)）',cont[2])[0]
                except:
                    metal_name = cont[2][:-3].strip()
                    area = '天津保定'
                metal_list = response.css('div.part3 table tr')
                for metal in metal_list:
                    if metal.css('td').extract():
                        item = LingtongItem()
                        item['web_name'] = 'lingtong'
                        item['area'] = area
                        item['metal'] = metal_name
                        item['date'] = pub_time
                        item['unit'] = unit
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
