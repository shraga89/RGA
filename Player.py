from config import *
import random
from abc import abstractmethod
import pandas as pd


class Player:
    def __init__(self, id, _type, budget, products, setting_initial_prices='random'):
        self.id = id
        self.type = _type
        self.price_limits = {} # key is tuple (product, selling\buying price)
        self.price_history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'outcome',
                                                   'actual_price', 'selling_price', 'buying_price'])
        self.current_prices = {} # key is tuple (product, selling\buying price)
        self.budget = budget
        self.all_existing_products = products
        self.products_in_inventory = [{p: 0 for p in products}, ]
        for p in products:
            self.set_initial_prices(p, setting_initial_prices)

    def set_initial_prices(self, product, method = 'random'):
        if method == "random":
            return self.set_random_initial_prices(product)
        else:
            raise ValueError("Illegal method of defining initial prices")

    def set_random_initial_prices(self, product):
        if 'buyer' not in self.type:
            self.price_limits[(product, 'selling_price')] = random.randint(MINIMAL_SELLING_PRICE, MAXIMAL_SELLING_PRICE)
            # self.price_history['selling_price'][product] = [
            #     random.randint(self.price_limits['selling_price'][product], MAXIMAL_SELLING_PRICE), ]
            # self.price_history['buying_price'][product] = [MINIMAL_BUYING_PRICE - 1, ]
            current_price = random.randint(self.price_limits[(product, 'selling_price')], MAXIMAL_SELLING_PRICE)
            self.current_prices[(product, 'selling_price')] = current_price
            self.price_history = self.price_history.append({'turn': 0,
                                                            'buyer': None,
                                                            'seller': self.id,
                                                            'product': product,
                                                            'outcome': 'initial',
                                                            'actual_price': None,
                                                            'selling_price': current_price,
                                                            'buying_price': MINIMAL_BUYING_PRICE - 1},
                                                           ignore_index=True)
            self.price_limits[(product, 'buying_price')] = MINIMAL_BUYING_PRICE - 1
        if 'seller' not in self.type:
            self.price_limits[(product, 'buying_price')] = random.randint(MINIMAL_BUYING_PRICE, MAXIMAL_BUYING_PRICE)
            # self.price_history['buying_price'][product] = [
            #     random.randint(self.price_limits['buying_price'][product], MAXIMAL_BUYING_PRICE), ]
            # self.price_history['selling_price'][product] = [MAXIMAL_BUYING_PRICE + 1, ]
            current_price = random.randint(MINIMAL_BUYING_PRICE, self.price_limits[(product, 'buying_price')])
            self.current_prices[(product, 'buying_price')] = current_price
            self.price_history = self.price_history.append({'turn': 0,
                                                            'buyer': self.id,
                                                            'seller': None,
                                                            'product': product,
                                                            'outcome': 'initial',
                                                            'actual_price': None,
                                                            'selling_price': MAXIMAL_BUYING_PRICE + 1,
                                                            'buying_price': current_price},
                                                           ignore_index=True)
            self.price_limits[(product, 'selling_price')] = MAXIMAL_BUYING_PRICE + 1

    def get_prices_by_time(self, timestamp=0):
        buying_price = dict()
        selling_price = dict()
        if 'buyer' not in self.type:
            for product in self.all_existing_products:
                # buying_price[product] = self.price_history['buying_price'][product][timestamp]
                selling_price[product] = self.price_history[
                    (self.price_history['product'] == product)
                    & (self.price_history['seller'] == self.id)
                    & (self.price_history['turn'] == timestamp)]['selling_price'].drop_duplicates().tolist()[0]
        if 'seller' not in self.type:
            for product in self.all_existing_products:
                buying_price[product] = self.price_history[
                    (self.price_history['product'] == product)
                    & (self.price_history['buyer'] == self.id)
                    & (self.price_history['turn'] == timestamp)]['buying_price'].drop_duplicates().tolist()[0]
        return {'buying_price': buying_price, 'selling_price': selling_price}

    def get_price_history_by_product(self, product):
        buying_prices = self.price_history[
            (self.price_history['product'] == product)
            & (self.price_history['buyer'] == self.id)].sort_values('turn')['buying_price'].drop_duplicates().tolist()
        selling_prices = self.price_history[
            (self.price_history['product'] == product)
            & (self.price_history['seller'] == self.id)].sort_values('turn')['selling_price'].drop_duplicates().tolist()
        return {'buying_price': buying_prices, 'selling_price': selling_prices}

    def get_current_selling_price(self, product):
        return self.current_prices[(product, 'selling_price')]

    def get_current_buying_price(self, product):
        return self.current_prices[(product, 'buying_price')]

    def get_id(self):
        return self.id

    @abstractmethod
    def set_current_prices(self):
        pass

    def add_inventory(self, product, amount):
        self.products_in_inventory[-1][product] += amount

    def update_history(self, history):
        # for record in history:
        #     if self.id in (record['seller'], record['buyer']):
        #         self.price_history['actual_price'][record['product']].append(record['product']['actual_price'])
        #         self.price_history['selling_price'][record['product']].append(record['product']['selling_price'])
        #         self.price_history['buying_price'][record['product']].append(record['product']['buying_price'])
        # if self.type == 'buyer':
        #     self.price_history['actual_price'][record['product']].append(None)
        #     self.price_history['selling_price'][record['product']].append(None)
        #     # should we save selling\buying prices of unsuccessful transactions
        #     self.price_history['buying_price'][record['product']].append(
        #         self.price_history['buying_price'][record['product']][-1])
        if 'buyer' not in self.type:
            projected_history = history[(history['seller'] == self.id)]
            self.price_history = pd.concat([self.price_history, projected_history])
        if 'seller' not in self.type:
            projected_history = history[(history['buyer'] == self.id)]
            self.price_history = pd.concat([self.price_history, projected_history])

    def get_last_transaction(self):
        pass

    def __repr__(self):
        to_print = f"{self.type} \nname: {self.id} \n"
        for product in self.all_existing_products:
            if 'seller' not in self.type:
                to_print += f'  will not sell {product} \n'
            else:
                to_print += f"  will sell {product} for at least {self.price_limits[(product, 'selling_price')]}$ \n"
            if 'buyer' not in self.type:
                to_print += f'  will not buy {product} \n'
            else:
                to_print += f"  will buy {product} for at most {self.price_limits[(product, 'buying_price')]}$ \n"
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

    def __init__(self, id, _type, budget, products, price_step = 1):
        super(RationalPlayer, self).__init__(id, _type, budget, products)
        self.price_step = price_step

    def set_current_prices(self):
        if 'seller' not in self.type:
            for product in self.all_existing_products:
                self.set_buying_price(product)
        if 'buyer' not in self.type:
            for product in self.all_existing_products:
                self.set_selling_price(product)

    def set_selling_price(self, product, is_versatile=False):
        last_price = self.get_current_selling_price(product)
        is_transaction_last_turn = 'successful' in self.price_history[
            (self.price_history['turn'] == self.price_history['turn'].max()) &
            (self.price_history['product'] == product)]['outcome'].tolist()
        possible_to_increase = last_price + self.price_step <= MAXIMAL_SELLING_PRICE
        possible_to_decrease = last_price - self.price_step >= self.price_limits[(product, 'selling_price')]
        if is_transaction_last_turn and possible_to_increase:
            self.current_prices[(product, 'selling_price')] += self.price_step
        elif possible_to_decrease:
            self.current_prices[(product, 'selling_price')] -= self.price_step

    def set_buying_price(self, product, is_versatile=False):
        last_price = self.get_current_buying_price(product)
        is_transaction_last_turn = 'successful' in self.price_history[
            (self.price_history['turn'] == self.price_history['turn'].max()) &
            (self.price_history['product'] == product)]['outcome'].tolist()
        possible_to_increase = last_price + self.price_step <= self.price_limits[(product, 'buying_price')]
        possible_to_decrease = last_price - self.price_step >= MINIMAL_BUYING_PRICE
        if is_transaction_last_turn and possible_to_decrease:
            self.current_prices[(product, 'buying_price')] -= self.price_step
        elif possible_to_increase:
            self.current_prices[(product, 'buying_price')] += self.price_step


class ProductionConsumptionPlayer(Player):

    def __init__(self, id, _type, budget, products, initial_production_price: dict, initial_consumption_utility: dict):
        super().__init__(id, _type, budget, products)
        # TODO: UPDATE price_history
        self.price_history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'outcome',
                                                   'actual_price', 'selling_price', 'buying_price'])
        for p in products:
            self.set_initial_prices(p)
        self.production_prices = []
        self.consumption_utilities = []
        if 'seller' not in self.type:
            self.production_prices.append(initial_production_price)
        if 'buyer' not in self.type:
            self.consumption_utilities.append(initial_consumption_utility)

    def set_initial_prices(self, product, method = 'random'):
        self.set_random_initial_prices(product)

    @abstractmethod
    def produce_inventory(self, product):
        pass
        # self.products_in_inventory[-1][product] += amount


class NaiveProductionConsumptionPlayer(ProductionConsumptionPlayer):

    def __init__(self, id, _type, budget, products, initial_production_price: dict, initial_consumption_utility: dict):
        super().__init__(id, _type, budget, products, initial_production_price, initial_consumption_utility)

    def produce_inventory(self, product):
        self.products_in_inventory[product].append(self.products_in_inventory[-1][product])
        if random.random() > 0.5 and self.budget > self.production_prices[-1]:
            self.products_in_inventory[-1][product] += 1
            self.budget -= self.products_in_inventory[-1][product]

