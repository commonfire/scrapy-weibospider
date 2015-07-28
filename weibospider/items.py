# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from  scrapy import Field,Item

class WeibospiderItem(Item):
    # define the fields for your item here like:
    content = Field()
    time = Field()
    atuser = Field()
    repostuser = Field()
    followuidlist = Field()
    userinfo =Field()
    #content_second = Field()
    #time_second = Field()
    #content_third = Field()
    #time_third = Field()
