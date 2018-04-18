# __author__ = "Amos"
# Email: 379833553@qq.com

import pymysql
from Data.settings import MYSQL_HOST,MYSQL_USERNAME,MYSQL_DB_NAME,MYSQL_PASSWORD,INIT_TIME
import time


def select_update_time(table_name,field_name='datetime'):
    try:
        client = pymysql.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, password=MYSQL_PASSWORD, database=MYSQL_DB_NAME)
        cursor = client.cursor()
        sql = "select %s from `%s` order by %s DESC LIMIT 1;" %(field_name,table_name,field_name)
        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            t = str(result[0])
            return time.mktime(time.strptime(t,'%Y-%m-%d'))
        else:
            if table_name in INIT_TIME.keys():
                if INIT_TIME[table_name]:
                    ss = time.mktime(time.strptime(INIT_TIME[table_name],'%Y-%m-%d'))
                else:
                    ss = None
                return ss
            else:
                raise ValueError('无法查询到时间，配置或输入错误，请检查')
    except:
        raise ValueError('表名错误，表%s不存在' %table_name)