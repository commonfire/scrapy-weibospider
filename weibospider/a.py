#-*-coding:utf-8 -*-
from pyquery import PyQuery as pq
import re
#d=pq('<p>hello//<a>hello</a>//<a>hello</a></p>')
#a=d('p').find('a').text()
#a=d('p').text()
d=pq('<p>testhello</p>')
a='testdouble'
#a=a.split() #split by space
#print a 


html ='<div class="abc"><div class="WB_text W_f14">repost<a target="_blank" render="ext" extra-data="type=atname" href="http://weibo.com/n/%E7%A7%92%E6%8B%8D?from=feed&amp;loc=at" usercard="name=秒拍">@秒拍</a><a target="_blank" render="ext" extra-data="type=atname" href="http://weibo.com/n/%E5%8E%A6%E9%97%A8%E6%A0%A1%E5%9B%AD?from=feed&amp;loc=at" usercard="name=厦门校园">@厦门校园</a>//<a target="_blank" render="ext" extra-data="type=atname" href="http://weibo.com/n/%E4%B8%9C%E5%93%A5byr?from=feed&amp;loc=at" usercard="name=东哥byr">@东哥byr</a></div></div><div class="abc"><div class="bcd"><div class="def">this is result<li><span>nickname</span><span>realname</span></li><li>2-li</li></div></div></div>'
#p=re.compile('(.*?@(.+?)</a>)+//(.*@(.+?)</a>)',re.S)

html2 ='<div class="PCD_person_info"><a class="WB_cardmore S_txt1 S_line1 clearfix" href="/p/1006051227086635/info?mod=pedit_more" bpfilter="page_frame" ontouchstart=""></a><div>'

d=pq(html2)
x=d("div.PCD_person_info").children('a').attr('href')
print 'result',x


#x=d('div.abc').children('.bcd').children('.def').find('li')
#print 'result:',x.eq(0).find('span').eq(0).text()
#y=pq(x).find('a').text()
#print y

#p=re.compile('(<a.*</a>)//(.*@(.+?)</a>)',re.S)
p=re.compile('.*//(.*@(.+?)</a>)',re.S)
match = p.search(x.html())
#print match.group(1)
d=pq(match.group(2))                                                                                                        
y=d.find('a').text().split('@')
#print match.group(2)

#print match.group(1),match.group(3)

#print match.group(2),match.group(4)

z='@abc@def'


