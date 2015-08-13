# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from  scrapy import Field,Item

class WeibospiderItem(Item):
    # define the fields for your item here like:
    uid = Field()
    content = Field()
    time = Field()
    atuser = Field()
    repostuser = Field()
    followuidlist = Field()
    userinfo =Field()
    
    image_urls = Field()
    images = Field()
