# -*- coding: utf-8 -*-

import json
import os.path as path
import codecs


def process():
    if not path.isfile('c5game_items.json'):
        return

    if not path.isfile('steam_items.json'):
        return

    c5game_file = open('c5game_items.json', 'rb')
    c5game_lines = c5game_file.readlines()

    steam_file = open('steam_items.json', 'rb')
    steam_lines = steam_file.readlines()
    # improve performance
    steam_set = set()

    diff_file = codecs.open('diff.json', mode='wb', encoding='utf-8')

    for steam_line in steam_lines:
        steam_obj = json.loads(steam_line)
        steam_item_name = steam_obj['item_name']
        steam_item_price = float(steam_obj['item_price'])

        if steam_item_price >= 1.0:
            steam_set.add(steam_item_name)

    for c5game_line in c5game_lines:
        c5game_obj = json.loads(c5game_line)
        c5game_item_name, c5game_item_link, c5game_item_price = [
            c5game_obj[key] for key in c5game_obj
        ]
        c5game_price_float = float(c5game_item_price)

        if c5game_item_name in steam_set and c5game_price_float >= 1.0:
            for steam_line in steam_lines:
                steam_obj = json.loads(steam_line)
                steam_item_name, steam_item_link, steam_item_price = [
                    steam_obj[key] for key in steam_obj
                ]
                steam_price_float = float(steam_item_price)
                price_higher = max(c5game_price_float, steam_price_float)

                if steam_item_name == c5game_item_name:
                    price_diff = abs(c5game_price_float - steam_price_float)
                    diff = zip([
                        'name', 'price_diff', 'price_ratio', 'steam_link',
                        'c5game_link'
                    ], [
                        steam_item_name,
                        float('%.2f' % price_diff), '%' + str(
                            float('%.2f' % (price_diff / price_higher)) * 100),
                        steam_item_link, c5game_item_link
                    ])
                    diff_line = json.dumps(diff) + '\n'
                    diff_file.write(diff_line.decode('unicode_escape'))

    steam_file.close()
    c5game_file.close()
    diff_file.close()


if __name__ == '__main__':
    process()
