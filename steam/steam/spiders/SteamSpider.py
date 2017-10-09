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

# *********************************************************
# 修改汇率
exchange_rate = 6.65

# *********************************************************


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
        '156c4f9a6afe2016bc38ab93',
        'Steam_Language':
        'english',
        'steamCountry':
        'CN%7C22a811fbd75798f1bbc28c37b7065273',
        'timezoneOffset':
        '28800,0',
        '_ga':
        'GA1.2.1288366058.1506504681',
        '_gid':
        'GA1.2.1170234144.1507271149',
        'steamLogin':
        '76561198073303687%7C%7CF63537B71C5C03B9EC1929BFE41D34DA102E5EC7'
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
        # yield Request(self.start_urls[0], headers=self.headers, meta={'cookiejar': '1'}, cookies=self.cookies, callback=self.parse)
        yield Request(self.start_urls[0], callback=self.parse)

    def parse(self, response):
        resp = Selector(text=json.loads(response.body)['results_html'])
        info_grp = resp.xpath('//a')

        for info in info_grp:
            item = SteamItem()
            rmb_str = info.xpath(
                'div[contains(@class, "market_listing_row")]/div[contains(@class, "market_listing_price_listings_block")]/div[contains(@class, "market_listing_right_cell")]/span[contains(@class, "market_table_value")]/span[@class="normal_price"]/text()'
            ).extract()[0]
            rmb_str = rmb_str.split(' ')[0]
            rmb_str = rmb_str.strip().replace(',', '')
            rmb_str = rmb_str[1:]
            # TODO 用rmb 显示价格之后要用去掉 unicode 字符串的方式来格式化价格
            # rmb_str = rmb_str.decode('unicode_escape').encode('ascii','ignore')
            rmb = float(rmb_str) * exchange_rate
            rmb = float('%.2f' % rmb)
            item['item_link'] = info.xpath('@href').extract()[0].strip()
            item['item_price'] = rmb
            item['item_name'] = info.xpath(
                'div[contains(@class, "market_listing_row")]/div[contains(@class, "market_listing_item_name_block")]/span[@class="market_listing_item_name"]/text()'
            ).extract()[0].strip()
            yield item

        for idx in page_list:
            next_url = base_url_first_part + str(
                idx * 10) + base_url_second_part
            # yield Request(next_url, headers=self.headers, meta={'cookiejar': response.meta['cookiejar']}, cookies=self.cookies, callback=self.parse)
            yield Request(next_url, callback=self.parse)
