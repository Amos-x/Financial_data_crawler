# -*- coding: utf-8 -*-
import scrapy
import time
from Data.items import ExbxgItem
from Data.utils import select_update_time
from urllib.parse import urlencode
import json


class ExbxgSpider(scrapy.Spider):
    name = 'exbxgSpider'
    init_url = 'https://www.exbxg.com:8443/jsonp?'
    today_time = time.time()

    def start_requests(self):
        """初始时间为：2011-01-01 16：00：00  """
        start_time = select_update_time('new_exbxg')
        t = int(time.time() * 1000)
        if start_time:
            date = time.strftime('%Y-%m-%d',time.localtime(start_time+86400))
        else:
            date = ''
        data = {
            'callback': 'jQuery110207587501276632844_%s' % (t - 1002),
            '{"timestamp":%s,"service":"U_D_FindSteel","body":{"beginDate":"%s","endDate":"","limit":10000}}' %(t,date): '',
            '_': '%s' % (t - 1000)
        }
        url = self.init_url + urlencode(data)
        yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        """判断并解析网页数据"""
        result = json.loads(response.text[46:-2])['data']['result']
        for x in result:
            item = ExbxgItem()
            item['time'] = time.strftime('%Y-%m-%d',time.localtime(x['date']/1000))
            item['web_name'] = 'exbxg'
            item['lowNickelCostPrice'] = x['lowNickelCostPrice']/100
            item['highNickelCostPrice'] = x['highNickelCostPrice']/100
            item['stainlessPrice'] = x['stainlessPrice']/100
            item['lowNickelWuxiPrice'] = x['lowNickelWuxiPrice']/100
            item['highNickelWuxiPrice'] = x['highNickelWuxiPrice']/100
            yield item
