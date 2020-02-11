from config import *
import random
from abc import abstractmethod


class Player:
    def __init__(self, id, _type, budget, products, setting_initial_prices='random'):
        self.id = id
        self.type = _type
        self.price_limits = {'buying_price': {}, 'selling_price': {}}
        self.price_history = {'buying_price': {}, 'selling_price': {}}
        self.budget = budget
        self.all_existing_products = products
        self.products_in_inventory = [{p: 0 for p in products}, ]
        for p in products:
            self.set_initial_prices(p, setting_initial_prices)

    def set_initial_prices(self, product, method):
        if method == "random":
            return self.set_random_initial_prices(product)
        else:
            raise ValueError("Illegal method of defining initial prices")

    def set_random_initial_prices(self, product):
        if 'buyer' not in self.type:
            self.price_limits['selling_price'][product] = random.randint(MINIMAL_SELLING_PRICE, MAXIMAL_SELLING_PRICE)
            self.price_history['selling_price'][product] = [random.randint(self.price_limits['selling_price'][product], MAXIMAL_SELLING_PRICE), ]
            self.price_history['buying_price'][product] = [MINIMAL_BUYING_PRICE - 1,]
            self.price_limits['buying_price'][product] = MINIMAL_BUYING_PRICE - 1
        if 'seller' not in self.type:
            self.price_limits['buying_price'][product] = random.randint(MINIMAL_BUYING_PRICE, MAXIMAL_BUYING_PRICE)
            self.price_history['buying_price'][product] = [random.randint(self.price_limits['buying_price'][product], MAXIMAL_BUYING_PRICE), ]
            self.price_history['selling_price'][product] = [MAXIMAL_BUYING_PRICE + 1,]
            self.price_limits['selling_price'][product] = MAXIMAL_BUYING_PRICE + 1

    def get_prices_by_time(self, timestamp=-1):
        buying_price = dict()
        selling_price = dict()
        for product in self.price_history['buying_price'].keys():
            buying_price[product] = self.price_history['buying_price'][product][timestamp]
        for product in self.price_history['selling_price'].keys():
            buying_price[product] = self.price_history['selling_price'][product][timestamp]
        return {'buying_price': buying_price, 'selling_price': selling_price}

    def get_price_history_by_product(self, product):
        buying_prices = self.price_history['buying_price'][product]
        selling_prices = self.price_history['selling_price'][product]
        return {'buying_price': buying_prices, 'selling_price': selling_prices}

    def get_current_selling_price(self, product):
        return self.get_price_history_by_product(product)['selling_price'][-1]

    def get_current_buying_price(self, product):
        return self.get_price_history_by_product(product)['buying_price'][-1]

    def get_id(self):
        return self.id

    @abstractmethod
    def set_current_prices(self):
        pass

    def add_inventory(self, product, amount):
        self.products_in_inventory[-1][product] += amount

    def update_history(self, history: list):
        for record in history:
            if record['buyer'] == self.id:
                self.price_history['buying price'][record['product']].append(
                    self.price_history['buying price'][record['product']][-1])
            if record['buyer'] == self.id:
                self.price_history['buying price'][record['product']].append(
                    self.price_history['buying price'][record['product']][-1])

    def __repr__(self):
        to_print = f"{self.type} \nname: {self.id} \n"
        for product in self.all_existing_products:
            if 'seller' not in self.type:
                to_print += f'  will not sell {product} \n'
            else:
                to_print += f"  will sell {product} for at least {self.price_limits['selling_price'][product]}$ \n"
            if 'buyer' not in self.type:
                to_print += f'  will not buy {product} \n'
            else:
                to_print += f"  will buy {product} for at most {self.price_limits['buying_price'][product]}$ \n"
        return to_print

    def has_product_available(self, product):
        return self.products_in_inventory[-1][product] != 0


class ConstantPricePlayer(Player):
    """
    A player that does not change prices
    """
    def __init__(self, id, _type, budget, products):
        super(ConstantPricePlayer, self).__init__(id, _type, budget, products)
        self.type = "ConstantPricePlayer " + self.type

    def set_current_prices(self):
        return self.get_prices_by_time()


class RationalPlayer(Player):
    """
    Player that behaves exactly like in the video
    """
    def __init__(self, id, _type, budget, products):
        super(RationalPlayer, self).__init__(id, _type, budget, products)

    def set_current_prices(self):
        if 'seller' not in self.type:
            self.set_buying_price()
        if 'buyer' not in self.type:
            self.set_selling_price()

    def set_selling_price(self):
        pass

    def set_buying_price(self):
        pass



