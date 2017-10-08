# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class C5GameItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    item_name = scrapy.Field()
    item_link = scrapy.Field()
    item_price = scrapy.Field()
