# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapytestItem(scrapy.Item):
    url = scrapy.Field()
    _id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    num_word = scrapy.Field()
    press = scrapy.Field()
    num_rate = scrapy.Field()
    rate = scrapy.Field()
    tag = scrapy.Field()
    img = scrapy.Field()
    des = scrapy.Field()
    price = scrapy.Field()
    similar = scrapy.Field()
    # releasedate = scrapy.Field()
