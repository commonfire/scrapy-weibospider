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
list = d.find('a').text()
for item in a:
    if item == '//':
        print 'exist'

html ='<div class="WB_text W_f14">repost<a target="_blank" render="ext" extra-data="type=atname" href="http://weibo.com/n/%E7%A7%92%E6%8B%8D?from=feed&amp;loc=at" usercard="name=秒拍">@秒拍</a><a target="_blank" render="ext" extra-data="type=atname" href="http://weibo.com/n/%E5%8E%A6%E9%97%A8%E6%A0%A1%E5%9B%AD?from=feed&amp;loc=at" usercard="name=厦门校园">@厦门校园</a>//<a target="_blank" render="ext" extra-data="type=atname" href="http://weibo.com/n/%E4%B8%9C%E5%93%A5byr?from=feed&amp;loc=at" usercard="name=东哥byr">@东哥byr</a></div>'
#p=re.compile('(.*?@(.+?)</a>)+//(.*@(.+?)</a>)',re.S)
d=pq(html)
x=d('div.WB_text')
#print x.html()
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
print re.split('@(\w*?)',z)


