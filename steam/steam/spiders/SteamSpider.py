# -*- coding: utf-8 -*-

import scrapy
from steam.items import SteamItem
from scrapy.http import Request, FormRequest
import json
from scrapy.http import TextResponse
from scrapy.selector import Selector

base_url_first_part = 'http://steamcommunity.com/market/search/render/?query=&start='
base_url_second_part = '&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any'
page_list = range(1, 950)

class SteamSpider(scrapy.Spider):
    name = "steam"
    allowed_domains = ["steamcommunity.com"]
    start_urls = [
        'http://steamcommunity.com/market/search/render/?query=&start=0&count=10&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730&category_730_ItemSet%5B%5D=any&category_730_ProPlayer%5B%5D=any&category_730_StickerCapsule%5B%5D=any&category_730_TournamentTeam%5B%5D=any&category_730_Weapon%5B%5D=any'
    ]

    cookies = {
        'recentlyVisitedAppHubs':
        '730',
        'sessionid':
        # '156c4f9a6afe2016bc38ab93',
        'cf462d4f652d82a745ba736e',
        # 'Steam_Language':
        # 'english',
        'timezoneOffset':
        '28800,0',
        '_ga':
        # 'GA1.2.1288366058.1506504681',
        'GA1.2.430351300.1507694096',
        '_gid':
        # 'GA1.2.1170234144.1507271',
        'GA1.2.148176026.1507694096',
        'steamCountry':
        # 'CN%7Cbe125ca12951334d20a1d1ea3d2f6029',
        'CN%7Cc90071f0d232df415b9349372022f897',
        'steamLogin':
        # '76561198073303687%7C%7CD37E5FD541EA9F875D5F7E91A0A51CC806BADEC6',
        '76561198398578329%7C%7C81D5487E8148D9270AF250BB7021FFF33C140687',
        'steamRememberLogin':
        # '76561198073303687%7C%7C4ac821fa709d8d44992c69733a07a2b0'
        '76561198398578329%7C%7C5a692010ccfe3a39289cfaadb139381a'
    }

    headers = {
        'Accept':
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding':
        'gzip, deflate, br',
        'Accept-Language':
        'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
        'Cache-Control':
        'max-age=0',
        'Connection':
        'keep-alive',
        'Host':
        'steamcommunity.com',
        'Referer':
        'http://steamcommunity.com/market/',
        'Upgrade-Insecure-Requests':
        '1',
        'User-Agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36'
    }

    def start_requests(self):
        yield Request(self.start_urls[0], headers=self.headers, meta={'cookiejar': '1'}, cookies=self.cookies, callback=self.parse)
        # yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        resp = Selector(text=json.loads(response.body)['results_html'])
        info_grp = resp.xpath('//a')

        for info in info_grp:
            item = SteamItem()
            rmb_str = info.xpath(
                'div[contains(@class, "market_listing_row")]/div[contains(@class, "market_listing_price_listings_block")]/div[contains(@class, "market_listing_right_cell")]/span[contains(@class, "market_table_value")]/span[@class="normal_price"]/text()'
            ).extract()[0]
            item['item_link'] = info.xpath('@href').extract()[0].strip()
            item['item_price'] = rmb_str.strip().replace(',', '')
            item['item_name'] = info.xpath(
                'div[contains(@class, "market_listing_row")]/div[contains(@class, "market_listing_item_name_block")]/span[@class="market_listing_item_name"]/text()'
            ).extract()[0].strip()
            yield item

        for idx in page_list:
            next_url = base_url_first_part + str(
                idx * 10) + base_url_second_part
            yield Request(next_url, headers=self.headers, meta={'cookiejar': response.meta['cookiejar']}, cookies=self.cookies, callback=self.parse)
            # yield Request(next_url, callback=self.parse)
