# -*- coding: utf-8 -*-

import scrapy
from c5game.items import C5GameItem
from scrapy.http import Request
import re

base_url = 'https://www.c5game.com'


class C5GameSpider(scrapy.Spider):
    pattern = re.compile(r'^\d+\.\d+$')
    name = "c5game"
    allowed_domains = ["c5game.com"]
    start_urls = [
        'https://www.c5game.com/csgo/default/result.html',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_knife&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_pistol&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_rifle%7Ccsgo_type_sniperrifle&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_smg&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_shotgun&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=type_hands&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_tool_weaponcase_keytag&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_weaponcase&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_tool_sticker&page=1',
        'https://www.c5game.com/csgo/default/result.html?type=csgo_type_musickit%7Ccsgo_type_collectible%7Ccsgo_tool_name_tagtag%7Ccsgo_type_spray&page=1'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)

    def parse(self, response):
        info_grp = response.xpath('//ul[contains(@class, "list-item4")]/li')
        next_url_suffix = response.xpath(
            '//ul[contains(@class, "pagination")]/li[contains(@class, "next")]/a/@href'
        ).extract()[0]

        for info in info_grp:
            item = C5GameItem()
            item['item_name'] = info.xpath(
                'p[@class="name"]/a/span/text()').extract()[0].strip()
            item['item_link'] = base_url + info.xpath(
                'a/@href').extract()[0].strip()
            # item_price_str = info.xpath('p[@class="info"]/span[@class="pull-left"]/span/text()').extract()[0].decode('unicode_escape').encode('ascii','ignore')
            item_price_str = info.xpath(
                'p[@class="info"]/span[@class="pull-left"]/span/text()'
            ).extract()[0]
            item_price_str = item_price_str.strip().replace(',', '')
            item['item_price'] = item_price_str
            yield item

        next_url = base_url + next_url_suffix
        yield Request(next_url, callback=self.parse)
