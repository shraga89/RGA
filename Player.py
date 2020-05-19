from config import *
import random
from abc import abstractmethod
import pandas as pd
from Knapsack import NaiveKnapsack


class Player:
    def __init__(self, id, _type, products,
                 setting_initial_prices='random'):
        self.id = id
        self.type = _type
        self.price_limits = {}  # key is tuple (product, selling\buying price)
        self.price_history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'outcome',
                                                   'actual_price', 'selling_price', 'buying_price'])
        self.current_prices = {}  # key is tuple (product, selling\buying price)
        self.all_existing_products = products
        self.products_in_inventory = [{p: 0 for p in products}, ]
        self.last_price = {}
        self.initial_prices = {}
        for p in products:
            initial_price = self.set_initial_prices(p, setting_initial_prices)
            self.initial_prices[p] = initial_price



    def retrieve_price_history(self, product) -> list:
        price_history = self.price_history[
            (self.price_history['outcome'] == 'successful') & (self.price_history['product'] == product)].sort_values(
            "turn")["actual_price"].values
        return price_history

    def set_initial_prices(self, product, method='random'):
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
        return current_price
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

    def __init__(self, id, _type, budget, products, price_step=1):
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


class DataPlayer(Player):

    def __init__(self, id, _type, products,  horizon):
        super().__init__(id, _type, products)
        # TODO: UPDATE price_history
        self.price_history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'outcome',
                                                   'actual_price', 'selling_price', 'buying_price'])
        # for p in products:
        #     self.set_initial_prices(p)
        self.production_prices = []
        self.consumption_utilities = []
        self.horizon = horizon

    def set_initial_prices(self, product, method='random'):
        return self.set_random_initial_prices(product)

    @abstractmethod
    def set_buying_price(self, product):
        pass

    @abstractmethod
    def set_selling_price(self, product):
        pass

    @abstractmethod
    def update_budget(self):
        pass

    def set_current_prices(self):
        if 'seller' not in self.type:
            for product in self.all_existing_products:
                self.set_buying_price(product)
        if 'buyer' not in self.type:
            for product in self.all_existing_products:
                self.set_selling_price(product)


class DataProvider(DataPlayer):

    def __init__(self, id, products, relevant_products, horizon):
        super().__init__(id, 'seller', products, horizon)
        self.selling_strategy = None
        self.relevant_products = relevant_products
        self.sold_last_turn = {}

        for p in self.relevant_products:
            self.products_in_inventory[-1][p]=1
            self.sold_last_turn[p]=False

    def set_selling_strategy(self, strategy):
        self.selling_strategy = strategy

    def gather_data(self, product):
        gathering_price = self.production_prices[-1][product]
        product_in_inventory = self.products_in_inventory[-1][product] == 1
        if random.random() > 0.0 and self.budget >= gathering_price and not product_in_inventory:
            self.products_in_inventory[-1][product] = 1
            self.budget -= gathering_price

    def is_product_relevant(self, product):
        return product in self.relevant_products and self.products_in_inventory[-1][product] == 1

    def set_buying_price(self, product):
        pass

    def update_budget(self):  # exisits for the sake of possible future directions
        self.budget = self.budget

    def set_selling_prices(self,turn,noise_sd):
        for product in self.relevant_products:
            updated_price = self.selling_strategy.set_selling_price(initial_price=self.initial_prices[product],num_of_turn=turn,total_turns=self.horizon,step=1,sold_last_turn=self.sold_last_turn[product],last_price=self.current_prices[(product,"selling_price")],noise_sd=noise_sd)
            self.current_prices[(product,"selling_price")] = updated_price




class DataConsumer(DataPlayer):

    def __init__(self, id, budget, products, horizon):
        super(DataConsumer,self).__init__(id, 'buyer', products, horizon)
        self.product_turn_bought = {}  # what turn the product was bought
        self.cost_estimation_strategy = None
        self.valuations = None
        self.bid_strategy = None
        self.budget = budget
        self.costs_dict = {}

    def set_valuations(self,valuations):
        self.valuations = valuations

    def set_cost_estimation_strategy(self,
                                     strategy):  # sets the strategy class of player - enables to change strategies during simulation
        self.cost_estimation_strategy = strategy

    def determine_product_cost(self, product, rellevant_sellers,history,evaluations):
        costs = []
        costs_dict = {}
        for seller in rellevant_sellers:
            df = history[
                (history["product"] == product) & (history["seller"] == seller.get_id()) & (history["actual_price"].notnull())][
                ["turn", "actual_price"]]
            if df.empty:
                seller_price_history = []
            else:
                seller_price_history = df.apply(pd.to_numeric).groupby("turn").mean()["actual_price"].tolist()
            cost = self.cost_estimation_strategy.cost_estimation(price_history=seller_price_history,
                                                                 evaluation=evaluations[product])

            costs.append(cost)
            costs_dict[seller] = cost
        minimum_cost = min(costs)
        self.set_buying_price(product, minimum_cost)
        return minimum_cost,costs_dict

    def is_product_relevant(self, product):
        return product in self.relevant_products and self.budget >= self.get_current_buying_price(product) \
               and self.products_in_inventory[-1][product] == 0

    def set_buying_price(self, product, price):
        self.current_prices[(product, 'buying_price')] = price

    def set_selling_price(self, product):
        pass

    def update_budget(self):
        owned_product = [product for product in self.all_existing_products if self.products_in_inventory[-1][product]>0]
        for product in owned_product:
            self.budget += self.valuations[product]

    def get_owned_product_repr(self):
        repr = ""
        owned_products = [product for product in self.all_existing_products if self.products_in_inventory[-1][product]>0]
        for product in owned_products:
            repr+=str(product)+" "
        return repr

    def determine_relevant_products(self, turn,players,history):
        costs = {}
        if turn not in self.costs_dict:
            self.costs_dict[turn]={}
        products_not_owned = [product for product in self.all_existing_products if self.products_in_inventory[-1][product]<=0]
        knapsack = NaiveKnapsack(self,products_not_owned)
        evaluations = {product:self.valuations[product] * (self.horizon - turn) for product in products_not_owned}
        for product in products_not_owned:
            relevant_sellers = [seller for seller_id, seller in players['sellers'].items()
                                if seller.has_product_available(product)]
            if not relevant_sellers:
                continue
            product_cost,tmp_costs_dict = self.determine_product_cost(product, relevant_sellers,history,evaluations)
            costs[product] = product_cost
            self.costs_dict[turn][product]=tmp_costs_dict
        relevant_products = knapsack.solve(turn, self.horizon, costs,evaluations)
        return relevant_products
