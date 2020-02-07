from config import *
import random
from abc import abstractmethod

class Player:
    def __init__(self, id, _type, budget, products, price_setting_policy=None):
        self.id = id
        self.type = _type
        self.price_limits = {'buying_price': {}, 'selling_price': {}}
        self.price_history = {'buying_price': {}, 'selling_price': {}}
        self.budget = budget
        self.all_existing_products = products
        self.products_in_inventory = [{p: None for p in products}, ]
        for p in products:
            self.set_initial_prices(p)
        self.price_setting_policy = price_setting_policy

    def set_initial_prices(self, product, method='random'):
        if method == "random":
            return self.set_random_initial_prices(product)
        else:
            raise ValueError("Illegal method of defining initial prices")

    def set_random_initial_prices(self, product):
        if self.type != 'buyer':
            self.price_limits['selling_price'][product] = random.randint(MINIMAL_SELLING_PRICE, MAXIMAL_SELLING_PRICE)
            self.price_history['selling_price'][product] = [random.randint(self.price_limits['selling_price'][product], MAXIMAL_SELLING_PRICE), ]
            self.price_history['buying_price'][product] = [MINIMAL_BUYING_PRICE - 1,]
            self.price_limits['buying_price'][product] = MINIMAL_BUYING_PRICE - 1
        if self.type != 'seller':
            self.price_limits['buying_price'][product] = random.randint(MINIMAL_BUYING_PRICE, MAXIMAL_BUYING_PRICE)
            self.price_history['buying_price'][product] = [random.randint(self.price_limits['buying_price'][product], MAXIMAL_BUYING_PRICE), ]
            self.price_history['selling_price'][product] = [MAXIMAL_BUYING_PRICE + 1,]
            self.price_limits['selling_price'][product] = MAXIMAL_BUYING_PRICE + 1

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

    def set_current_prices(self):
        current_prices = self.price_setting_policy.set_prices(self)

    def __repr__(self):
        to_print = f"Player {self.id}: \n "
        for product in self.all_existing_products:
            to_print += f"  will sell {product} for at least {self.price_limits['selling_price'][product]}" \
                          f"\n   will buy {product} for at most {self.price_limits['buying_price'][product]} \n"

        return to_print

    class AbstractPriceSettingPolicy:
        @abstractmethod
        def set_prices(self, player):
            pass

    class RationalPriceSetting(AbstractPriceSettingPolicy):
        def set_prices(self, player):
            pass
            # TODO define a policy similar to what was shown in the video
