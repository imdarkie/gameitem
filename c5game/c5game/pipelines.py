# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import json
import codecs


class C5GamePipeline(object):
    def __init__(self):
        os.chdir('..')
        file_name = os.getcwd() + '/c5game_items.json'
        self.file = codecs.open(file_name, mode='wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + '\n'
        self.file.write(
            line.decode('unicode_escape').encode('ascii', 'ignore'))
        return item

    def spider_closed(self, spider):
        self.file.close()
