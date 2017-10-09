import json

def test_c5():
    c5game_file = open('c5game_items.json', 'rb')
    c5game_lines = c5game_file.readlines()

    c5 = 0
    for line in c5game_lines:
        c5 += 1
        c5game_obj = json.loads(line)
        c5game_item_price = c5game_obj['item_price']
        try:
            price = float(c5game_item_price)
        except ValueError:
            print(c5)

def test_steam():
    steam_file = open('steam_items.json', 'rb')
    steam_lines = steam_file.readlines()
    steam = 0
    for line in steam_lines:
        steam += 1
        steam_obj = json.loads(line)
        steam_item_price = steam_obj['item_price']
        try:
            price = float(steam_item_price)
        except ValueError:
            print(steam)

if __name__ == '__main__':
    test_c5()
    # test_steam()