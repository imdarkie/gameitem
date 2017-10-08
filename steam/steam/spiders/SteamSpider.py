# -*- coding: utf-8 -*-

import scrapy
from steam.items import SteamItem
from scrapy.http import Request
import json
from scrapy.http import TextResponse
from scrapy.selector import Selector


base_url_first_part = 'http://steamcommunity.com/market/search/render/?query=&start='
base_url_second_part = '&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any'
page_list = range(1, 20)

class C5GameSpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["steamcommunity.com"]
    start_urls = [
        'http://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any'
    ]

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        resp = Selector(text=json.loads(response.body)['results_html']) 
        info_grp = resp.xpath('//a')

        for info in info_grp:
            item = SteamItem()
            item['item_link'] = info.xpath('@href').extract()[0]
            item['item_price'] = info.xpath('div[contains(@class, "market_listing_row")]/div[contains(@class, "market_listing_price_listings_block")]/div[contains(@class, "market_listing_right_cell")]/span[contains(@class, "market_table_value")]/span[@class="normal_price"]/text()').extract()[0].split(" ")[0][1:]
            item['item_name'] = info.xpath('div[contains(@class, "market_listing_row")]/div[contains(@class, "market_listing_item_name_block")]/span[@class="market_listing_item_name"]/text()').extract()[0]
            yield item

        for idx in page_list:
            next_url = base_url_first_part + str(idx * 10) + base_url_second_part
            yield Request(next_url, callback=self.parse)
