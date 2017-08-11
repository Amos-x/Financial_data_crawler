# -*- coding: utf-8 -*-
import scrapy
import time
try:
    from Data.settings import START_DATE
except:
    START_DATE=None
from Data.items import DataItem


class ExbxgSpider(scrapy.Spider):
    name = 'exbxgSpider'
    # allowed_domains = ['www.exbxg.com']
    # start_urls = ['http://www.exbxg.com/']
    url = 'http://www.exbxg.com/hq/hq_day.php?date={date}'
    today_time = time.time()

    def start_requests(self):
        """初始时间为：2011-01-01 16：00：00  """
        if START_DATE:
            start_time = time.mktime(time.strptime(START_DATE,'%Y-%m-%d')) + 57600
        else:
            start_time = 1293811200.0 +57600
        while start_time < self.today_time:
            date_time = time.strftime('%Y-%m-%d', time.localtime(start_time))
            yield scrapy.Request(self.url.format(date=date_time),callback=self.parse,meta={'time':start_time})
            start_time += 86400

    def parse(self, response):
        """判断并解析网页数据"""
        tr_list = response.css('table tbody tr[prodtype="12"]')
        if tr_list:
            item = DataItem()
            type_name = ''
            for group in tr_list:
                td_list = group.css('td')
                if len(td_list) == 13:
                    type_name = td_list[0].css('::text').extract_first()
                    td_list = td_list[1:]
                item['web_name'] = 'exbxg'
                item['time'] = time.strftime('%Y-%m-%d',time.localtime(response.meta['time']))
                item['productname'] = type_name
                item['deliverymonth'] = td_list[0].css('span::text').extract_first()
                item['presettlementprice'] = td_list[1].css('::text').extract_first()
                openprice = td_list[2].css('::text').extract_first()
                item['openprice'] = (0 if '-' in openprice else openprice)
                highestprice = td_list[3].css('::text').extract_first()
                item['highestprice'] = (0 if '-' in highestprice else highestprice)
                lowestprice = td_list[4].css('::text').extract_first()
                item['lowestprice'] = (0 if '-' in lowestprice else lowestprice)
                item['closeprice'] = td_list[5].css('::text').extract_first()
                item['averageprice'] = td_list[6].css('::text').extract_first()
                zd1_chg = td_list[7].css('font::text').extract_first()
                item['zd1_chg'] = (0 if '-' in zd1_chg else zd1_chg)
                volume = td_list[8].css('::text').extract_first().strip()
                item['volume'] = (int(volume[:-1])*10000 if '万' in volume else volume)
                turnover = td_list[9].css('::text').extract_first().strip()
                if '万' in turnover:
                    item['turnover'] = float(turnover[:-1]) * 10000
                elif '亿' in turnover:
                    item['turnover'] = float(turnover[:-1]) * 100000000
                elif '-' in turnover:
                    item['turnover'] = 0
                else:
                    item['turnover'] = turnover
                openinterest = td_list[10].css('::text').extract_first()
                item['openinterest'] = (0 if '-' in openinterest else openinterest)
                item['openinterestchg'] = td_list[11].css('font::text').extract_first()
                yield item