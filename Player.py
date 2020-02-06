from config import *
import random

class Player:
    def __init__(self, id, _type, budget, products):
        self.id = id
        self.type = _type
        self.price_limits = {'buying_price': {}, 'selling_price': {}}
        self.price_history = {'buying_price': {}, 'selling_price': {}}
        self.budget = budget
        self.products = [{p: None for p in products}, ]
        for p in products:
            self.set_init_prices(p)

    def set_init_prices(self, product):
        if self.type != 'buyer':
            self.price_history['selling_price'][product] = [random.randint(min_selling_price, max_selling_price), ]
        if self.type != 'seller':
            self.price_history['buying_price'][product] = [random.randint(min_buying_price, max_buying_price), ]
