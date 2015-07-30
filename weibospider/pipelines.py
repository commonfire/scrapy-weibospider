# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from twisted.enterprise import adbapi
import logging
import MySQLdb
import sys
from scrapy.utils.project import get_project_settings
reload(sys)
sys.setdefaultencoding('utf8')


class WeibospiderPipeline(object):
    
    settings = get_project_settings()
    start_uid = settings['UID']

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
        d = self.dbpool.runInteraction(self._weiboinfo_insert,item,spider)  
        d.addErrback(self._handle_error,item,spider) 
        d.addBoth(lambda _:item)
        return d

    def _weiboinfo_insert(self,conn,item,spider):
        #if item.get('content') and item.get('time'):
        #插入发表微博内容和时间
        for i in range(len(item['content'])):
            if("'" in item['content'][i]):
                content_tmp = item['content'][i].replace("'","\\'")
                conn.execute("insert into t_user_weibo(userID,content,time,atuser,repostuser) values(%s,%s,%s,%s,%s)",(str(item['uid']),content_tmp,item['time'][i],item['atuser'][i],item['repostuser'][i]))
            else:
                conn.execute("insert into t_user_weibo(userID,content,time,atuser,repostuser) values(%s,%s,%s,%s,%s)",(str(item['uid']),item['content'][i],item['time'][i],item['atuser'][i],item['repostuser'][i]))
       #将微博用户个人信息插入数据库 

        #print '===============================',item['userinfo']

        conn.execute("insert into t_user_info(userID,userAlias,location,sex,blog,domain,brief,birthday,registertime) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(str(item['uid']),item['userinfo']['昵称：'.decode('utf-8')],item['userinfo']['所在地：'.decode('utf-8')],item['userinfo']['性别：'.decode('utf-8')],item['userinfo']['博客：'.decode('utf-8')],item['userinfo'.decode('utf-8')]['个性域名：'.decode('utf-8')],item['userinfo']['简介：'.decode('utf-8')],item['userinfo']['生日：'.decode('utf-8')],item['userinfo']['注册时间：'.decode('utf-8')]))

        #将微博用户的关注用户列表插入数据库
        for i in range(len(item['followuidlist'])):
            conn.execute("insert into t_user_follow(userID,followID) values(%s,%s)",(str(WeibospiderPipeline.start_uid),item['followuidlist'][i]))

    def _handle_error(self,failure,item,spider):
        logging.error(failure)


