# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import logging
import MySQLdb
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class WeibospiderPipeline(object):
    def __init__(self,dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls,settings):
        dbargs = dict(
            host = settings['MYSQL_HOST'],
            db = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            passwd = settings['MYSQL_PASSWD'],
            charset = 'utf8',
        )
        dbpool = adbapi.ConnectionPool('MySQLdb',**dbargs)
        return cls(dbpool)
    
    def process_item(self,item,spider):
        d = self.dbpool.runInteraction(self._content_time_insert,item,spider)  
        d.addErrback(self._handle_error,item,spider) 
        d.addBoth(lambda _:item)
        return d

    def _content_time_insert(self,conn,item,spider):
        '''插入发表微博内容和时间'''
        if item.get('content') and item.get('time'):
            for i in range(len(item['content'])):
                if("'" in item['content'][i]):
                    content_tmp = item['content'][i].replace("'","\\'")
                    conn.execute("insert into t_user_weibo(userID,content,time) values(%s,%s,%s)",(str(2728266823),content_tmp,item['time'][i]))
                else:
                    conn.execute("insert into t_user_weibo(userID,content,time) values(%s,%s,%s)",(str(2728266823),item['content'][i],item['time'][i]))

    def _handle_error(self,failure,item,spider):
        logging.error(failure)


