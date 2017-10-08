# -*- coding: utf-8 -*-

import scrapy
from c5game.items import C5GameItem
from scrapy.http import Request


base_url = 'https://www.c5game.com'

class C5GameSpider(scrapy.Spider):
    name = "c5game"
    allowed_domains = ["c5game.com"]
    start_urls = [
        'https://www.c5game.com/csgo/default/result.html'
    ]

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        info_grp = response.xpath('//ul[contains(@class, "list-item4")]/li')
        next_url_suffix = response.xpath('//ul[contains(@class, "pagination")]/li[@class="next"]/a/@href').extract()[0]

        for info in info_grp:
            item = C5GameItem()
            item['item_name'] = info.xpath('p[@class="name"]/a/span/text()').extract()[0]
            item['item_link'] = info.xpath('a/@href').extract()[0]
            item['item_price'] = info.xpath('p[@class="info"]/span[@class="pull-left"]/span/text()').extract()[0].split(" ")[0][1:]
            yield item

        next_url = base_url + next_url_suffix
        yield Request(next_url, callback=self.parse)

