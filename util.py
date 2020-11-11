import numpy as np
import pandas as pd

class Shop:

    def __init__(self, id, name, num_item):
        self.id       = id
        self.name     = name
        self.num_item = num_item
        self.items    = []
        self.queue    = []

    def __repr__(self):
        return '{}-"{}"-{}'.format(self.id, self.name, self.num_item)

def load_shops():
    shops = {}
    df = pd.read_csv('data/shop.csv')
    for _, (id, name, num_item) in df.iterrows():
        shop = Shop(id, name, num_item)
        shops[id] = shop
    return shops

class Item:

    def __init__(self, id, name, shop, requirements, time, price):
        self.id           = id
        self.name         = name
        self.shop         = shop
        self.requirements = requirements
        self.time         = time
        self.price        = price

    def __repr__(self):
        return '{}-"{}"-"{}"-{}-{} <- {}'.format(
                self.id, self.name, self.shop.name,
                self.time, self.price, self.requirements)

class Requirement:

    def __init__(self, item, num_item):
        self.item     = item
        self.num_item = num_item

    def __repr__(self):
        return '"{}"-{}'.format(self.item.name, self.num_item)

def load_requirements(items, requirement_string):
    requirements = []
    if type(requirement_string) is str:
        for _ in requirement_string.split('-'):
            item_id, num_item = _.split('|')
            item_id = int(item_id)
            item = items[item_id]
            requirement = Requirement(item, num_item)
            requirements.append(requirement)
    return requirements

def load_items(shops):
    items = {}

    df = pd.read_csv('data/item.csv')
    for _, (id, name, shop_id, requirements, time, price) in df.iterrows():
        shop = shops[shop_id]
        requirements = load_requirements(items, requirements)
        item      = Item(id, name, shop, requirements, time, price)
        shop.items.append(item)
        items[id] = item
    return items, shops

def choose_random_shop(shops):
    return shops[np.random.choice(np.arange(len(shops))) + 1]

def choose_random_item(items):
    return items[np.random.choice(np.arange(len(items)))]

def check_item(item, num_item):
    # initialization
    flag_valid = True

    # check constraint of this item
    if len(item.shop.queue) + num_item > int(item.shop.num_item):
        flag_valid = False
#        print('    - fail to add {} {} to {} {}/{}'.format(num_item, item.name,
#            item.shop.name, len(item.shop.queue), item.shop.num_item))
        return flag_valid

    # check requirement recursively
    for requirement in item.requirements:
        flag_valid = check_item(requirement.item, int(requirement.num_item))
        if not flag_valid:
            break

    return flag_valid

def add_item(item, num_item):
    # initialization
    flag_valid = True

    # add of this item
    for _ in range(num_item):
        item.shop.queue.append(item)

    # check requirement recursively
    for requirement in item.requirements:
        add_item(requirement.item, int(requirement.num_item))

def generate_random_solution(shops, items, patience=100):
    root_items = []

    while patience > 0:
        # break if factory is full
        factory = shops[1]
        if len(factory.queue) >= factory.num_item:
            break

        # generate random solution
        shop = choose_random_shop(shops)
        item = choose_random_item(shop.items)
        flag = check_item(item, 1)

        if not flag:
#            print('adding {} to {} failed'.format(item.name, shop.name))
            patience -= 1
        else:
            add_item(item, 1)
            root_items.append(item)
#            print('adding {} to {}'.format(item.name, shop.name))
    return shops, items, root_items

def get_total_price(root_items):
    total_price = 0
    for item in root_items:
        total_price += item.price
    return total_price

def get_item_time(item):
    # set time of this item
    total_time = item.time

    # set time recursively
    max_requirement_time = 0
    for requirement in item.requirements:
        requirement_time = get_item_time(requirement.item)
        if requirement_time > max_requirement_time:
            max_requirement_time = requirement_time

    # add requirement time
    total_time += max_requirement_time
    return total_time

def get_inteval(root_items):
    inteval = 0
    for item in root_items:
        total_time = get_item_time(item)
        if total_time > inteval:
            inteval = total_time
    return inteval

