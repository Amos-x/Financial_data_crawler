# Financial_data_crawler
爬取国内一些交易所的金融数据

爬取的网站如下：  
1.中国金融期货交易所  
2.郑州商品交易所   
3.大连商品交易所   
4.中国不锈钢交易网   
5.上海黄金交易所   
6.上海期货交易所  
7.长江现货
8.上海现货铝价
9.佛山灵通金属报价
  
## 使用说明

#### 1.执行数据库脚本，创建数据库表
    数据库脚本位于init_sql文件夹中


#### 2.修改配置
##### settings.py 文件中修改如下内容    
数据库连接：    
    
    MYSQL_HOST = 'localhost'
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = 'wyx379833553'
    MYSQL_DB_NAME = 'tianyi'


#### 3.运行
##### 1.单线程（推荐）
直接执行run.py即可使用。


##### 2.多进程
多进程需要使用redis作为去去重调度库，需要修改settings.py，取消如下注释，并修改redis连接地址
    
    #SCHEDULER = "scrapy_redis.scheduler.Scheduler"
    #DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
    #REDIS_URL = 'redis://DESKTOP-V9EPT1L:wyx379833553@localhost:6379'
    #SCHEDULER_PERSIST = True
    #SCHEDULER_IDLE_BEFORE_CLOSE = 30
    
然后修改run.py文件使用多进程，并启动。

    #r = scheduler()
    #r.run()