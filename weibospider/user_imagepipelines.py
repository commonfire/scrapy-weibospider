#-*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem

class UserImagesPipeline(ImagesPipeline):
    
    def get_media_requests(self,item,info):
            image_url = item['image_urls']
            yield scrapy.Request(image_url)

    def item_completed(self,results,item,info):
        image_paths = [x['path'] for isTrue,x in results if isTrue]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
