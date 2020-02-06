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
            self.set_initial_prices(p)

    def set_initial_prices(self, product, method):
        if method == "random":
            return self.set_random_initial_prices(product)
        else:
            raise ValueError("Illegal method of defining initial prices")

    def set_random_initial_prices(self, product):
        if self.type != 'buyer':
            self.price_history['selling_price'][product][0] = [random.randint(MINIMAL_SELLING_PRICE, MAXIMAL_SELLING_PRICE), ]
            self.price_history['buying_price'][product][0] = [MINIMAL_BUYING_PRICE - 1,]
            self.price_limits['buying_price'][product] = [MINIMAL_BUYING_PRICE - 1,]
        if self.type != 'seller':
            self.price_history['buying_price'][product][0] = [random.randint(MINIMAL_BUYING_PRICE, MAXIMAL_BUYING_PRICE), ]
            self.price_history['selling_price'][product][0] = [MAXIMAL_BUYING_PRICE + 1,]
            self.price_limits['selling_price'][product] = [MAXIMAL_BUYING_PRICE + 1,]

    def get_prices_by_time(self, timestamp):
        buying_price = dict()
        selling_price = dict()
        for product in self.price_history['buying_price'].keys():
            buying_price[product] = self.price_history['buying_price'][product][-1]
        for product in self.price_history['selling_price'].keys():
            buying_price[product] = self.price_history['selling_price'][product][-1]
        return {'buying_price': buying_price, 'selling_price': selling_price}

    def get_price_history_by_product(self, product):
        buying_prices = self.price_history['buying_price'][product]
        selling_prices = self.price_history['selling_price'][product]
        return {'buying_price': buying_prices, 'selling_price': selling_prices}
