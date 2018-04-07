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
from Data.spiders.czceSpider import CzcespiderSpider
from Data.spiders.ccmn import CcmnSpider
from Data.spiders.cnal import CnalSpider
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


# 单机单进程爬去启动类
class scheduler02(object):

    def run(self):
        process = CrawlerProcess()
        process.crawl(CffexSpider)
        process.crawl(DecspiderSpider)
        process.crawl(ExbxgSpider)
        process.crawl(SgeSpider)
        process.crawl(ShfeSpider)
        process.crawl(CzcespiderSpider)
        process.crawl(CcmnSpider)
        process.crawl(CnalSpider)
        process.start()


if __name__ == '__main__':
    # 单机多进程分布爬取
    # r = scheduler()
    # r.run()

    # 这里用单机单进程爬取
    s = scheduler02()
    s.run()
