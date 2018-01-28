import os
from multiprocessing import Process
try:
    from Data.settings import CORE_NUMBER
except:
    CORE_NUMBER=None
from scrapy.crawler import CrawlerProcess
from Data.spiders.cffexSpider import CffexSpider
from Data.spiders.decSpider import DecspiderSpider
from Data.spiders.exbxgSpider import ExbxgSpider
from Data.spiders.sgeSpider import SgeSpider
from Data.spiders.shfeSpider import ShfeSpider
import time


class scheduler(object):
    """
    一个单机多进程爬取启动类
    """

    def __init__(self):
        self.core_number = CORE_NUMBER

    @staticmethod
    def crawl():
        os.system('scrapy crawl lingtong')

    def run(self):
        names = locals()
        if self.core_number:
            for x in range(self.core_number):
                names['process%x' % x] = Process(target=scheduler.crawl)
                names['process%x' % x].start()


if __name__ == '__main__':
    # 单机多进程分布爬取
    r = scheduler()
    r.run()