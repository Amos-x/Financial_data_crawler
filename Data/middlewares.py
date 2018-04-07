# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import time
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse
import requests
from bs4 import BeautifulSoup
import re
from Data.get_lingtong_coookie import GetLingTongCookie


class DataSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class LonglongLoginMiddleware(object):
    """
    用于灵通金属报价网站的登陆，获取cookie，并保存，知道cookie失效再次重新获取。
    """

    def __init__(self):
        self.path = 'C:\\Users\Amos\PycharmProjects\Data\Data\lingtong_cookie'
        with open(self.path) as f:
            content = f.read()
            cookie = eval(content)
        params = {'datew': time.strftime('%Y-%m-%d', time.localtime(time.time()))}
        response = requests.get('http://lingtong.info/gb/price.asp',cookies=cookie, params=params)
        if response.status_code == '500':
            print('cookie失效')
            self.cookie = GetLingTongCookie().get_cookie()
        else:
            print('cookie有效')
            self.cookie = cookie

    def process_request(self,request,spider):
        request.cookies = self.cookie
