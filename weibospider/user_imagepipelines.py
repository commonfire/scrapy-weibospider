#-*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
import re

class UserImagesPipeline(ImagesPipeline):
   
    def file_path(self,request,response=None,info=None):
        p = re.compile('.cn/(\d*?)/')
        match = p.search(request.url)
        if(match):
            return 'full/%s.jpg' % match.group(1)
        else:
            print 'file_path--url_wrong!!'
    
    def get_media_requests(self,item,info):
        image_url = item['image_urls']
        yield scrapy.Request(image_url)

    def item_completed(self,results,item,info):
        image_paths = [x['path'] for isTrue,x in results if isTrue]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
