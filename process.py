# -*- coding: utf-8 -*-

import json
import os.path as path


def process():
    c5game_data = None

    if not path.isfile('c5game_items.json'):
        return

    if not path.isfile('steam_items.json'):
        return

    c5game_file = open('c5game_items.json')
    c5game_lines = c5game_file.readlines()

    steam_file = open('steam_items.json', 'rb')
    steam_lines = steam_file.readlines()
    # improve performance
    steam_set = set()

    for steam_line in steam_lines:
        steam_obj = json.loads(steam_line)
        steam_item_name = steam_obj['item_name']
        steam_set.add(steam_item_name)

    for c5game_line in c5game_lines:
        c5game_obj = json.loads(c5game_line)
        c5game_item_name = c5game_obj['item_name']

        if c5game_item_name in steam_set:
            print(c5game_item_name)

            for steam_line in steam_lines:
                steam_obj = json.loads(steam_line)
                steam_item_name = steam_obj['item_name']
                
                if steam_item_name == c5game_item_name:
                    print(steam_obj['item_price'])

    steam_file.close()
    c5game_file.close()


if __name__ == '__main__':
    process()
