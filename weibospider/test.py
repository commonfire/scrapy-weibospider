#-*-coding:utf-8 -*-
import getinfo


#f = open('./followflag.txt','w')
#f.write('hello\n2222\n')
#a='hi'
#b='zjd'
#getinfo.set_followflag('./followflag.txt',a,b)
#c,d =  getinfo.get_followflag('./followflag.txt')
#print

#class test:
#    data = {
#        'name':''
#     }
#
#    def changeValue(self):
#        test.data['name']='zjd'
#
#
#t = test()
#t.changeValue()
#print test.data['name']
a = {}.fromkeys(('昵称：'.decode('utf-8'),'所在地：','性别：','博客：','个性域名：','简介：','生日：','注册时间：'),' ')
print a.keys()
