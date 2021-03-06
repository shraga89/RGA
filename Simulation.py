from abc import abstractmethod
import random
import pandas as pd
from Knapsack import NaiveKnapsack
from Contract import *
import os
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
            print_df = print_df[print_df['turn'] == turn]
        else:
            print("-------------------------")
        # print(print_df.to_string() if len(print_df) > 0 else '')
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

    def __init__(self, horizon, product_list, players_dict, contract: Contract,noise_sd):
        super().__init__(horizon, product_list, players_dict)
        self.history = pd.DataFrame(columns=['turn', 'buyer', 'seller', 'product', 'actual_price','budget'])
        self.budget_history = pd.DataFrame(columns=['turn', 'buyer','budget','owned_products'])
        self.price_predictions = pd.DataFrame(columns=['turn', 'buyer','seller','product','estimated_cost',"real_cost"])
        self.turn = 0
        self.contract = contract
        self.noise_sd=noise_sd

    def create_inventory(self):
        for seller in self.players['sellers'].values():
            for product in seller.relevant_products:
                seller.gather_data(product)


    def print_df_results(self,fname,df):
        print_df = df.copy()
        print_df.to_csv(fname)

    def run_simulation(self,offset,simulation_number,output_folder):
        current_output_folder = output_folder+"/"+str(offset)+"/"
        if not os.path.exists(current_output_folder):
            os.makedirs(current_output_folder)
        for t in range(self.horizon):
            self.run_one_step()
            self.turn += 1
        self.print_df_results(current_output_folder+"/budget_results_"+str(simulation_number)+".csv",self.budget_history)
        self.print_df_results(current_output_folder+"/estimation_results_"+str(simulation_number)+".csv",self.price_predictions)


    def reset_selling_indicator(self):
        for seller in self.players["sellers"]:
            for product in self.players["sellers"][seller].sold_last_turn:
                self.players["sellers"][seller].sold_last_turn[product]=False

    def run_one_step(self):
        relevant_buyers = {}
        self.reset_selling_indicator()
        for buyer in set(self.players['buyers'].values()):
            buyer.update_budget() # This is done prior to the round in order to count only product purchased in previous rounds
            relevant_products = buyer.determine_relevant_products(self.turn, self.players,self.history)
            for product in relevant_products:
                if product not in relevant_buyers:
                    relevant_buyers[product] = [buyer]
                else:
                    relevant_buyers[product].append(buyer)

        self.update_dataframes()
        for product in self.product_list:
            if product not in relevant_buyers:
                continue
            self.run_one_step_for_single_product(product, relevant_buyers[product])
        for seller in self.players["sellers"]:
            self.players["sellers"][seller].set_selling_prices(self.turn,self.noise_sd)

        # for buyer in set(self.players['buyers'].values()):
        #
        #     self.budget_history = self.budget_history.append({"turn":self.turn,
        #                                                       "buyer":buyer.get_id(),
        #                                                       "budget":buyer.budget,
        #                                                       'owned_products':buyer.get_owned_product_repr()
        #                                                       },ignore_index=True)


    def update_dataframes(self):
        for buyer in set(self.players['buyers'].values()):
            self.budget_history = self.budget_history.append({"turn": self.turn,
                                                              "buyer": buyer.get_id(),
                                                              "budget": buyer.budget,
                                                              'owned_products': buyer.get_owned_product_repr()
                                                              }, ignore_index=True)
            for product in buyer.costs_dict[self.turn]:
                for seller in buyer.costs_dict[self.turn][product]:
                    real_selling_price = seller.get_current_selling_price(product)
                    self.price_predictions = self.price_predictions.append({"turn": self.turn,
                                                              "buyer": buyer.get_id(),
                                                              "seller":seller.get_id(),
                                                              "product": product,
                                                              "estimated_cost":buyer.costs_dict[self.turn][product][seller],
                                                              "real_cost":real_selling_price
                                                              }, ignore_index=True)

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
                    matched_seller.sold_last_turn[product]=True
                else:
                    buyers_dict[buyer].remove(matched_seller)
                    if not buyers_dict[buyer]:
                        buyers_dict.pop(buyer)

                self.add_transaction_to_history(buyer, matched_seller, product, price)

    def add_transaction_to_history(self, buyer, seller, product, price):
        self.history = self.history.append({"turn": self.turn,
                             'buyer': buyer.get_id(),
                             'seller': seller.get_id(),
                             'product': product,
                             'actual_price': price,
                             'budget':buyer.budget},
                            ignore_index=True)


    def visualize(self):
        pass
