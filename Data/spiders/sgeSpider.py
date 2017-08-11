# -*- coding: utf-8 -*-
#from urllib.parse import urljoin
import time
import scrapy
from Data.items import DataItem
from urllib.request import urljoin
import re
from bs4 import BeautifulSoup
try:
    from Data.settings import START_DATE
except:
    START_DATE = None

class SgeSpider(scrapy.Spider):
    name = 'sgeSpider'
    url ='http://www.sge.com.cn/sjzx/mrhqsj?p={page}'
    error = 0

    def start_requests(self):
        """请求日统计数据 第一页"""
        if START_DATE:
            yield scrapy.Request('http://www.sge.com.cn/sjzx/mrhqsj', callback=self.next_parse, dont_filter=True,meta={'page': 1})
        else:
            yield scrapy.Request('http://www.sge.com.cn/sjzx/mrhqsj',callback=self.first_parse,dont_filter=True)

    def first_parse(self, response):
        """获取数据总页数，并循环请求每个页面"""
        pages_all = response.css('div.pagination ul.clear li::text').extract()[-1]
        for page_num in range(1,int(pages_all)+1):
            yield scrapy.Request(self.url.format(page=page_num),callback=self.next_parse)

    def next_parse(self,response):
        """获取页面的 内容链接 列表"""
        if START_DATE:
            li_list = response.css('div.articleList ul li')
            for group in li_list:
                datetime = group.css('a span.fr::text').extract_first()
                if time.mktime(time.strptime(datetime,'%Y-%m-%d')) < time.mktime(time.strptime(START_DATE,'%Y-%m-%d')):
                    break
                url = group.css('a::attr(href)').extract_first()
                yield scrapy.Request(urljoin(response.url,url),callback=self.last_parse)
            lastdate = li_list[-1].css('a span.fr::text').extract_first()
            if time.mktime(time.strptime(lastdate, '%Y-%m-%d')) > time.mktime(time.strptime(START_DATE,'%Y-%m-%d')):
                yield scrapy.Request(self.url.format(page=response.meta['page']+1),callback=self.next_parse,meta={'page':response.meta['page']+1})
        else:
            urls = response.css('div.articleList ul li.lh45 a::attr(href)').extract()
            for url in urls:
                yield scrapy.Request(urljoin(response.url,url),callback=self.last_parse)

    def last_parse(self, response):
        """解析网页获取数据"""
        try:
            soup = BeautifulSoup(response.text,'lxml')
            tr_list = soup.select('div.content table tbody tr')
            if tr_list:
                item = DataItem()
                time = response.css('div.jzk_newsCenter_meeting div.title p')[0].css('::text').extract()[-1]
                for tr in tr_list[1:]:
                    td_list = [td.get_text().strip() for td in tr.select('td')]
                    length = len(td_list)
                    if length >=10:
                        item['web_name'] = 'sge'
                        item['time'] = time
                        item['productname'] = re.sub(r',','',td_list[0])
                        item['openprice'] = re.sub(r',','',td_list[1])
                        item['highestprice'] = re.sub(r',','',td_list[2])
                        item['lowestprice'] = re.sub(r',','',td_list[3])
                        item['closeprice'] = re.sub(r',','',td_list[4])
                        item['zd1_chg'] = td_list[5]
                        if length ==11:
                            item['averageprice'] = re.sub(r',','',td_list[6])
                            item['volume'] = re.sub(r',','',td_list[7])
                            item['turnover'] = re.sub(r',','',td_list[8])
                            item['openinterest'] = re.sub(r',', '', td_list[9])
                            item['deliverynum'] = (None if not td_list[10] else re.sub(r',', '', td_list[10]))
                        else:
                            item['zd2_chg'] = (float(td_list[6][:-1]) / 100 if '%' in td_list[6] else td_list[6])
                            item['averageprice'] = re.sub(r',', '', td_list[7])
                            item['volume'] = re.sub(r',', '', td_list[8])
                            item['turnover'] = re.sub(r',', '', td_list[9])
                            item['openinterest'] = None
                            item['deliverypoint'] = None
                            item['deliverynum'] = None
                            if length == 10:
                                item['highestprice'] = td_list[4].strip()
                                item['closeprice'] = td_list[2].strip()
                            if length == 12:
                                openinterest = td_list[10]
                                if len(openinterest)>1 and openinterest:
                                    item['openinterest'] = re.sub(r',', '', openinterest)
                                item['deliverynum'] = (None if not td_list[11] else re.sub(r',', '', td_list[11]))
                            if length == 13:
                                openinterest = td_list[10]
                                if len(openinterest) > 1 and openinterest:
                                    item['openinterest'] = re.sub(r',', '', openinterest)
                                item['deliverypoint'] = (None if not td_list[11] else re.sub(r',', '', td_list[11]))
                                item['deliverynum'] = (None if not td_list[12] else re.sub(r',', '', td_list[12]))
                        yield item
        except:
            # 这个网站数据结构多变，且不统一，会有一些久远的数据抓取不到。
            self.error +=1
            print('解析错误数:',self.error)
