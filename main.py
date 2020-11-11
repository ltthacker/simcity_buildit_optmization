import util
import numpy as np
from copy import deepcopy
from pprint import pprint

def objective_function(root_items):
    total_price = util.get_total_price(root_items)
    inteval     = util.get_inteval(root_items)
    if inteval == 0:
        return 0
    return - total_price # + np.abs(24 - inteval / 60) * 1500

def main():
    # load data
    shops = util.load_shops()
    _items, _shops = util.load_items(shops)


    # initialize
    best_objective = np.inf

    i = 0
    while 1:
        i += 1
        # get a copy of the original data
        shops = deepcopy(_shops)
        items = deepcopy(_items)

        # randomly generate a solution
        shops, items, root_items = util.generate_random_solution(shops, items)

        # calculate objective value
        objective = objective_function(root_items)

        if objective < best_objective:
            print('[+] trial {} found new solution:'.format(i))
            for shop in shops.values():
                print('    -', shop.name)
                print('        +', '-'.join('"{}"'.format(_.name) for _ in shop.queue))
            print('[+] root items:')
            for item in root_items:
                print('    - {}'.format(item.name))

            total_price = util.get_total_price(root_items)
            inteval     = util.get_inteval(root_items)
            print('[+] Total price:', total_price)
            print('[+] Inteval    :', inteval / 60)
            print('[+] Objective  :', objective)

            best_objective = objective
        else:
            if i % 1000 == 0:
                print('[+] trial {}: {}'.format(i, objective))



if __name__ == '__main__':
    main()
