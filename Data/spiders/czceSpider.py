# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from Data.items import DataItem
import re

class CzcespiderSpider(scrapy.Spider):
    name = 'czceSpider'
    # allowed_domains = ['www.czce.com.cn']
    start_urls = ['http://www.czce.com.cn/portal/jysj/qhjysj/mrhq/A09112001index_1.htm']
    url = 'http://www.czce.com.cn/portal/jysj/qhjysj/mrhq/A09112001index_1.htm'

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser,10)
        self.today_time = time.time()

    def spider_close(self):
        self.browser.quit()

    def parse(self, response):
        self.browser.get(self.url)
        input_window = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'table tbody input#pubDate')))
        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'table tbody img#button')))
        start_time = 1104508800.0 +57600     #1072886400.0 + 57600
        while start_time < self.today_time:
            datetime = time.strftime('%Y-%m-%d',time.localtime(start_time))
            input_window.clear()
            input_window.send_keys(datetime)
            button.click()
            handles = self.browser.window_handles
            self.browser.switch_to_window(handles[-1])
            html = self.browser.page_source
            self.html_parse(html=html,time=datetime)

            print('- ',datetime)
            self.browser.close()
            self.browser.switch_to_window(handles[0])
            start_time += 86400


    def html_parse(self,html,time):
        print('1')
        soup = BeautifulSoup(html,'lxml')
        tr_list = soup.select('table tbody tr')
        if tr_list:
            print('2')
            item = DataItem()
            type_name =''
            for tr in tr_list[1:]:
                td_list = [td.get_text().strip() for td in tr.select('td')]
                item['time'] = time
                type_name = (type_name if len(td_list[0])==2 else td_list[0][:2])
                item['productname'] = type_name
                item['deliverymonth'] = td_list[0]
                item['presettlementprice'] = (None if not td_list[1] else re.sub(r',','',td_list[1]))
                item['openprice'] = (None if not td_list[2] else re.sub(r',','',td_list[2]))
                item['highestprice'] = (None if not td_list[3] else re.sub(r',','',td_list[3]))
                item['lowestprice'] = (None if not td_list[4] else re.sub(r',','',td_list[4]))
                item['closeprice'] = (None if not td_list[5] else re.sub(r',','',td_list[5]))
                item['settlementprice'] = (None if not td_list[6] else re.sub(r',','',td_list[6]))
                if len(td_list) ==13:
                    a = 0
                    item['zd1_chg'] = None
                    item['zd2_chg'] = (None if not td_list[7] else re.sub(r',','',td_list[7]))
                if len(td_list) ==14:
                    a = 1
                    item['zd1_chg'] = (None if not td_list[7] else re.sub(r',','',td_list[7]))
                    item['zd2_chg'] = (None if not td_list[8] else re.sub(r',','',td_list[8]))
                item['volume'] = (None if not td_list[8+a] else re.sub(r',','',td_list[8+a]))
                item['openinterest'] = (None if not td_list[9+a] else re.sub(r',','',td_list[9+a]))
                item['openinterestchg'] = (None if not td_list[10+a] else re.sub(r',','',td_list[10+a]))
                item['turnover'] = (None if not td_list[11+a] else re.sub(r',','',td_list[11+a]))
                item['deliveryprice'] = (None if not td_list[12+a] else re.sub(r',','',td_list[12+a]))
                item['web_name'] = 'czce'
                yield item
