# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from items import ScrapytestItem

class ScrapytestPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["book"]
        self.book = db["book"]

    def process_item(self, item, spider):

        """ 判断类型 存入MongoDB """
        if isinstance(item, ScrapytestItem):
            try:
                self.book.insert(dict(item))
            except Exception:
                pass

        return item
