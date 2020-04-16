from abc import abstractmethod
import random
import pandas as pd
from Knapsack import NaiveKnapsack
from Contract import *
from random import shuffle, randint


class Simulation:
    def __init__(self, horizon, product_list, players_dict):
        self.horizon = horizon
        self.players = players_dict
        self.product_list = product_list
        self.history = pd.DataFrame()

    @abstractmethod
    def run_simulation(self):
        pass

    @abstractmethod
    def visualize(self):
        pass

    def print_end_result(self, success_only=True, export=None, turn=None):
        print_df = self.history.copy()
        if type(turn) == int:
            print(f"turn number {turn}")
            print("-------------------------")
            print_df = print_df[print_df['turn'] == turn]
        else:
            print(f"full horizon")
            print("-------------------------")
        # if success_only:
        #     print_df = print_df[print_df['outcome'] == 'successful']
        print(print_df.to_string() if len(print_df) > 0 else '')
        if export:
            print_df.to_csv(export)


class NaiveSimulation(Simulation):
    def __init__(self, horizon, product_list, players_dict):
        super().__init__(horizon, product_list, players_dict)
        self.history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'outcome',
                                             'actual_price', 'selling_price', 'buying_price'])
        self.turn = 1
        self.create_inventory()

    def create_inventory(self):
        for seller in self.players['sellers'].values():
            for product in self.product_list:
                seller.add_inventory(product, self.horizon)

    def run_simulation(self):
        for t in range(self.horizon):
            self.run_one_step()
            self.print_end_result(True, None, self.turn)
            self.turn += 1
        self.print_end_result(False, 'sim.csv', None)

    def run_one_step(self):
        for product in self.product_list:
            self.run_one_step_for_single_product(product)
        for player in set(self.players['buyers'].values()).union(self.players['sellers'].values()):
            player.update_history(self.history[self.history['turn'] == self.turn])
            player.set_current_prices()

    def run_one_step_for_single_product(self, product):

        sellers_list = [seller_id for seller_id, seller in self.players['sellers'].items()
                        if seller.has_product_available(product)]
        buyers_list = list(buyer_id for buyer_id in self.players['buyers'].keys())
        buyers_dict = {buyer: sellers_list.copy() for buyer in buyers_list}

        while buyers_list:
            buyer = random.sample(buyers_list, 1)[0]
            random.shuffle(buyers_dict[buyer])
            seller = buyers_dict[buyer].pop()
            if self.create_transaction(self.players['sellers'][seller], self.players['buyers'][buyer], product):
                buyers_dict.pop(buyer)
                buyers_list.remove(buyer)
                sellers_list.remove(seller)

                for a_buyer, available_sellers in list(buyers_dict.items()):
                    try:
                        available_sellers.remove(seller)
                    except ValueError:
                        pass
            for a_buyer, available_sellers in list(buyers_dict.items()):
                if len(available_sellers) == 0:
                    buyers_dict.pop(a_buyer)
            buyers_list = list(buyers_dict.keys())

    def create_transaction(self, seller, buyer, product):
        actual_price = seller.get_current_selling_price(product)
        if actual_price > buyer.get_current_buying_price(product):
            self.history = self.history.append({'turn': self.turn,
                                                'buyer': buyer.get_id(),
                                                'seller': seller.get_id(),
                                                'product': product,
                                                'outcome': 'unsuccessful',
                                                'actual_price': None,
                                                'selling_price': seller.get_current_selling_price(product),
                                                'buying_price': buyer.get_current_buying_price(product)},
                                               ignore_index=True)
            return False
        elif actual_price > buyer.budget:
            self.history = self.history.append({'turn': self.turn,
                                                'buyer': buyer.get_id(),
                                                'seller': seller.get_id(),
                                                'product': product,
                                                'outcome': 'no budget',
                                                'actual_price': None,
                                                'selling_price': seller.get_current_selling_price(product),
                                                'buying_price': buyer.get_current_buying_price(product)},
                                               ignore_index=True)
            return False
        else:
            seller.add_inventory(product, -1)
            buyer.add_inventory(product, 1)
            seller.budget += actual_price
            buyer.budget -= actual_price
            self.history = self.history.append({'turn': self.turn,
                                                'buyer': buyer.get_id(),
                                                'seller': seller.get_id(),
                                                'product': product,
                                                'outcome': 'successful',
                                                'actual_price': actual_price,
                                                'selling_price': seller.get_current_selling_price(product),
                                                'buying_price': buyer.get_current_buying_price(product)},
                                               ignore_index=True)
            return True

    def visualize(self):
        pass


class DataMarketSimulation(Simulation):

    def __init__(self, horizon, product_list, players_dict, contract: Contract):
        super().__init__(horizon, product_list, players_dict)
        self.history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'actual_price'])
        self.turn = 0
        self.contract = contract

    def create_inventory(self):
        for seller in self.players['sellers'].values():
            for product in seller.relevant_products:
                seller.gather_data(product)

    def run_simulation(self):
        for t in range(self.horizon):
            self.run_one_step()
            self.print_end_result(True, None, self.turn)
            self.turn += 1
        self.print_end_result(False, 'sim.csv', None)

    def run_one_step(self):
        relevant_buyers = {}
        for buyer in set(self.players['buyers'].values()):
            relevant_products = buyer.determine_relevant_products(self.turn, self.players,self.history)
            for product in relevant_products:
                if product not in relevant_buyers:
                    relevant_buyers[product] = [buyer]
                else:
                    relevant_buyers[product].append(buyer)

        for product in self.product_list:
            if product not in relevant_buyers:
                continue
            self.run_one_step_for_single_product(product, relevant_buyers[product])

    def run_one_step_for_single_product(self, product, relevant_buyers):
        sellers_list = [seller for seller_id, seller in self.players['sellers'].items()
                        if seller.has_product_available(product)]
        buyers_dict = {buyer: list(sellers_list) for buyer in relevant_buyers}
        while buyers_dict:
            for buyer in list(buyers_dict.keys()):
                matched_seller = random.choice(buyers_dict[buyer])
                transaction_indicator, outcome = self.contract.check_prerequisites([matched_seller, buyer], product)
                price = None
                if transaction_indicator:
                    price = self.contract.enact_contract([matched_seller, buyer], product)
                    buyers_dict.pop(buyer)
                else:
                    buyers_dict[buyer].remove(matched_seller)
                    if not buyers_dict[buyer]:
                        buyers_dict.pop(buyer)

                self.add_transaction_to_history(buyer, matched_seller, product, price)

    def add_transaction_to_history(self, buyer, seller, product, price):
        self.history = self.history.append({"turn": self.turn,
                             'buyer': buyer,
                             'seller': seller.get_id(),
                             'product': product,
                             'actual_price': price},
                            ignore_index=True)


    def visualize(self):
        pass
