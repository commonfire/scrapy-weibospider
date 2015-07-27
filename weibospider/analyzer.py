# -*- coding: utf-8 -*-   
import re
import json
from pyquery import PyQuery as pq

class Analyzer:
    '''网页内容分析'''
    def __init__(self):
        self.content_list = []      #微博内容列表
        self.time_list = []         #微博发表时间列表
        self.atuser_list = []       #记录用户微博@用户
        self.repostuser_list = []   #记录微博转发用户
        self.follower_list = []     #某用户粉丝列表
        self.follow_list = []       #某用户关注列表
        self.childfollow_list = []  #某子用户关注列表
	

#########################################获取个人主页内容#################################
    def get_mainhtml(self,total): 
        '''获取个人主页中html内容'''
        total_pq = pq(unicode(total))  
	    #获取指定<script>
        total1 = total_pq('script:contains("WB_feed WB_feed_profile")').html()   
	    #利用正则匹配出大括号内的内容（json串）
        p=re.compile('{.*}',re.S)
        match = p.search(unicode(total1)) 
        if match:
            data1=match.group() 
            data2=json.loads(data1)
            data3=data2['html'].decode('utf-8')
            total_pq = pq(unicode(data3))
            return total_pq
        else:
            print "getmainHtml wrong!"

    def get_content(self,total_pq):
        '''获取用户发表微博内容'''
        data = total_pq("div[node-type=feed_list_content]")
        for d in data :
            d = pq(d)
            content = d.contents()[0].strip()
            self.content_list.append(content)
        return self.content_list
	
    def get_time(self,total_pq):
        '''获取用户发表微博时间'''
        datatime = total_pq('div.WB_from')
        for dt in datatime:
            dt = pq(dt)
            if(dt.find('a').eq(0).attr('name')):  #注意不记录转发微博原文的发表时间
                time = dt.find('a').eq(0).attr('title')
                self.time_list.append(time)
        return self.time_list

    def get_atuser_repostuser(self,total_pq):
        '''获取用户微博中@的用户以及获取转发微博的一级源用户'''
        user = total_pq('div[node-type=feed_list_content]')
        for au in user:
            au = pq(au)
            #text_list = au.text().split()  #根据空格分割
            if '//' in au.text():     #存在转发可能
                p1 = re.compile('(<a.*?</a>)\s?//',re.S)
                match1 = p1.search(au.html())
                if match1:
                    atuser_list = pq(match1.group(1))('a').text()
                    self.atuser_list.append(atuser_list)
                else:
                    self.atuser_list.append('')
                    
                p2 = re.compile('.*?//(<a.*?@(.+?)</a>)',re.S)
                match2 = p2.search(au.html())
                if match2:
                    self.repostuser_list.append(match2.group(2))
                else:
                    self.repostuser_list.append('')

            else: 
                atuser_list1 = au.find('a').text()   #记录用户微博中的@用户
                #self.atuser_list.append([atuser_item[1:] for atuser_item in atuser_list1])
                self.atuser_list.append(atuser_list1)
                
                repostuser = au.parents('div.WB_detail')  #记录微博用户中的@用户，情况2：直接转发者
                ru = repostuser.find('div[node-type=feed_list_forwardContent]').find('a').eq(0).attr('nick-name') 
                if ru is not None:
                    self.repostuser_list.append(ru) 
                else:
                    self.repostuser_list.append('')
        return self.atuser_list,self.repostuser_list


######################################获取粉丝列表########################################
    def get_followerhtml(self,total):
        '''获取粉丝列表页面中html内容'''	
        total_pq = pq(unicode(total)) 
        total1 = total_pq('script:contains("info_name W_fb W_f14")').html()        
        p = re.compile('{.*}',re.S)
        match = p.search(unicode(total1))
        if match:
            data1=match.group()
            data2=json.loads(data1)
            data3=data2['html'].decode('utf-8')
            total_pq = pq(unicode(data3))
            return total_pq
        else:
            print "getfollowerHtml wrong!"

    def get_follower(self,total_pq):
        '''获取某用户的粉丝uid'''
        data = total_pq("div.info_name")
        for dflr in data:
            dflr = pq(dflr)
            flr_uid = dflr.find('a').eq(0).attr('usercard')
            p = re.compile('id=(\d*)')
            match = p.search(unicode(flr_uid))
            if match:
                self.follower_list.append(match.group(1))
            else:
                print "getFollower wrong!"
        return self.follower_list
	    

####################################获取关注列表###########################################
    def get_followhtml(self,total):
        '''获取关注列表页面中html内容'''
        total_pq = pq(unicode(total))
        total1 = total_pq('script:contains("title W_fb W_autocut")').html()
        p = re.compile('{.*}',re.S)
        match = p.search(unicode(total1))
        if match:
            data1=match.group()
            data2=json.loads(data1)
            data3=data2['html'].decode('utf-8')
            total_pq = pq(unicode(data3))
            return total_pq
        else:
            print "getfollowHtml wrong!"
    
    def get_follow(self,total_pq):
        '''获取某用户的关注uid'''
        data = total_pq("div.title")
        for dfl in data:
            dfl = pq(dfl)
            fl_uid = dfl.find('a').eq(0).attr('usercard')
            p = re.compile('id=(\d*)')
            match = p.search(unicode(fl_uid))
            if match:
                self.follow_list.append(match.group(1))
            else:
                print "getFollow wrong!"
        return self.follow_list

    def get_childfollowhtml(self,total):
        '''获得子用户的关注列表页面html'''
        total_pq = self.get_followerhtml(total)  #和获取粉丝列表页面的方法相同
        return total_pq

    def get_childfollow(self,total_pq):
        '''获得子用户的关注用户'''
        self.childfollow_list = self.get_follower(total_pq)
        return self.childfollow_list

