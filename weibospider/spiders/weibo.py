# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request,FormRequest
from scrapy.utils.project import get_project_settings
from weibospider.items import WeibospiderItem
import re
import base64
import rsa
import binascii
import time
import getinfo
from getpageload import GetWeibopage
from analyzer import Analyzer
from settings import USER_NAME

class WeiboSpider(CrawlSpider):
    name = 'weibo'
    allowed_domains = ['weibo.com','sina.com.cn']
    settings = get_project_settings()
    #start_username = settings['USER_NAME']
    start_username = USER_NAME
    start_password = settings['PASS_WORD']
    start_uid = settings['UID']
    page_num = settings['PAGE_NUM']
    filename  = settings['FILENAME']
    follow_page_num = settings['FOLLOW_PAGE_NUM']
    
    def start_requests(self):
        username = WeiboSpider.start_username
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=sso&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&client=ssologin.js(v1.4.4)' % username
        return [Request(url=url,method='get',callback=self.post_requests)]

    def post_requests(self,response):
        serverdata = re.findall('{"retcode":0,"servertime":(.*?),"pcid":.*?,"nonce":"(.*?)","pubkey":"(.*?)","rsakv":"(.*?)","exectime":.*}',response.body,re.I)[0]  #获取get请求的数据，用于post请求登录
        #print '!!!!GET responsebody:',response.body
        #print '!!!!serverdata',serverdata[0]
        servertime = serverdata[0]
        nonce = serverdata[1]
        pubkey = serverdata[2]
        rsakv = serverdata[3]
        username= WeiboSpider.start_username
        password = WeiboSpider.start_password
        formdata = {
            'entry': 'weibo',  
            'gateway': '1',  
            'from': '',  
            'ssosimplelogin': '1',  
            'vsnf': '1',  
            'vsnval': '',  
            'su': getinfo.get_user(username),  
            'service': 'miniblog',  
            'servertime': servertime,  
            'nonce': nonce,  
            'pwencode': 'rsa2',  
            'sp': getinfo.get_pwd(password,servertime,nonce,pubkey),  
            'encoding': 'UTF-8',  
            'prelt': '115',  
            'rsakv': rsakv, 
            'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack', 
            'returntype': 'META'
            }
        headers={'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'} 
        return [FormRequest(url='http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.4)',formdata=formdata,headers=headers,callback=self.get_cookie)]

     
    def get_cookie(self, response):
        #print 'response:~~~~~~~~~~~~~~~',response.body
        p = re.compile('location\.replace\(\'(.*)\'\)')
        try:
            login_url = p.search(response.body).group(1)
            #print '==============',login_url 
            ret_res = re.search('retcode=0',login_url)
            if ret_res:
                print 'Login Success!!!!'
            else:
                print 'Login Fail!!!!'
        except:
            print 'Login Error!!!!'

        request = response.request.replace(url=login_url,meta={'cookiejar':1},method='get',callback=self.get_userinfo)   #self.get_follow)   #GET请求login_url获取返回的cookie，后续发送Request携带此cookie
        return request

#######################################################################
    def get_userinfo(self,response):
        mainpageurl = 'http://weibo.com/u/'+str(1227086635)+'?from=otherprofile&wvr=3.6&loc=tagweibo'
        GetWeibopage.data['uid'] = 1227086635
        getweibopage = GetWeibopage()
        GetWeibopage.data['page'] = 1
        firstloadurl = mainpageurl + getweibopage.get_firstloadurl()
        yield  Request(url=firstloadurl,meta={'cookiejar':response.meta['cookiejar']},callback=self.get_userurl)

    def get_userurl(self,response):
        analyzer = Analyzer()
        total_pq =  analyzer.get_html(response.body,'script:contains("PCD_person_info")')
        userinfo_url = analyzer.get_userinfohref(total_pq)
        yield  Request(url=userinfo_url,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_userinfo)
        
    def parse_userinfo(self,response):
        f=open('./text1.html','w')
        f.write(response.body)

        analyzer = Analyzer()
        total_pq = analyzer.get_html(response.body,'script:contains("PCD_text_b")')
        userinfo_dict = analyzer.get_userinfo(total_pq)
        print '^^^^^^^^^^^^^^^^^user info',userinfo_dict
######################################################################
    def get_url(self,uid):
        '''获取入口uid的关注列表页面'''
        url = 'http://weibo.com/p/100505' + str(uid) + '/myfollow?' 
        return url

    def get_follow(self,response):
        formdata = {
            'cfs':'',
            't':'1',
            'Pl_Official_RelationMyfollow__104_page':'1'   
        }
        uid = '2728266823'
        follow_url = self.get_url(uid)
        #for page in range(WeiboSpider.follow_page_num):
            #print '************************pagenumber:',page+1
        #formdata['Pl_Official_RelationMyfollow__104_page'] = str(page+1)
        yield FormRequest(url=follow_url,formdata=formdata,meta={'cookiejar':response.meta['cookiejar'],'page':1},callback=self.parse_follow)


    def parse_follow(self,response):
        item = WeibospiderItem()
        analyzer = Analyzer()
        total_pq = analyzer.get_followhtml(response.body)
        item['followuidlist'] = analyzer.get_follow(total_pq) 
        oldflag = getinfo.get_followflag(WeiboSpider.filename)
        for follow_uid in item['followuidlist'][:2]:
            print '%%%%%%%%%%%%%%%%%%%%%%%%%%',follow_uid
            if follow_uid != oldflag:
                mainpageurl = 'http://weibo.com/u/'+str(follow_uid)+'?from=otherprofile&wvr=3.6&loc=tagweibo'
                GetWeibopage.data['uid'] = follow_uid
                getweibopage = GetWeibopage()
                for page in range(WeiboSpider.page_num):
                    GetWeibopage.data['page'] = page+1
                    firstloadurl = mainpageurl + getweibopage.get_firstloadurl()
                    yield  Request(url=firstloadurl,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_firstload)   #有问题
            else:
                break
        if response.meta['page'] == 1:
            getinfo.set_followflag(WeiboSpider.filename,item['followuidlist'][0])
        else:
           print 'page is not equal 1!!!!!!!!!!'

        for page in range(2,WeiboSpider.follow_page_num+1):  
            follow_url = self.get_url('2728266823')
            formdata = {
                'cfs':'',
                't':'1',
                'Pl_Official_RelationMyfollow__104_page':str(page)   
            }     
            yield FormRequest(url=follow_url,formdata=formdata,meta={'cookiejar':response.meta['cookiejar'],'page':page},callback=self.parse_follow)
        #return item     


    def start_getweiboinfo(self,response,follow_uid):
        mainpageurl = 'http://weibo.com/u/'+str(follow_uid)+'?from=otherprofile&wvr=3.6&loc=tagweibo'
        GetWeibopage.data['uid'] = follow_uid
        getweibopage = GetWeibopage()
        for page in range(WeiboSpider.page_num): 
            GetWeibopage.data['page'] = page+1
            firstloadurl = mainpageurl + getweibopage.get_firstloadurl()
            yield  Request(url=firstloadurl,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_firstload)

            secondloadurl = mainpageurl + getweibopage.get_secondloadurl()
            yield  Request(url=secondloadurl,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_secondload)
           
            thirdloadurl = mainpageurl + getweibopage.get_thirdloadurl()
            yield  Request(url=thirdloadurl,meta={'cookiejar':response.meta['cookiejar']},callback=self.parse_thirdload)
        
    def parse_firstload(self,response):
        item = WeibospiderItem()
        analyzer = Analyzer()
        total_pq =  analyzer.get_mainhtml(response.body)
        item['content'] = analyzer.get_content(total_pq)
        item['time'] = analyzer.get_time(total_pq)
        item['atuser'],item['repostuser'] = analyzer.get_atuser_repostuser(total_pq)
        return item


    def parse_secondload(self,response):
        item = WeibospiderItem()
        analyzer = Analyzer()
        total_pq =  analyzer.get_mainhtml(response.body)
        item['content'] = analyzer.get_content(total_pq)
        item['time'] = analyzer.get_time(total_pq)
        item['atuser'],item['repostuser'] = analyzer.get_atuser_repostuser(total_pq)
        return item


    def parse_thirdload(self,response):
        item = WeibospiderItem()
        analyzer = Analyzer()
        total_pq =  analyzer.get_mainhtml(response.body)
        item['content'] = analyzer.get_content(total_pq)
        item['time'] = analyzer.get_time(total_pq)
        item['atuser'],item['repostuser'] = analyzer.get_atuser_repostuser(total_pq)
        return item

        
