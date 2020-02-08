from config import *
from utils import *
import Player as pl
from abc import abstractmethod


class Simulation:
    def __init__(self):
        pass

    @abstractmethod
    def run_simulation(self):
        pass

    @abstractmethod
    def print_end_result(self):
        pass


# class UniformBudgetSimulation(Simulation):
#     def __init__(self, number_of_sellers, number_of_buyers, number_of_versatile_players, number_of_turns, budget, product_list):
#         self.players= {}
#         for i in range(number_of_buyers):
#             player_id = 'buyer_' + str(i)
#             self.players[player_id] = pl.ConstantPricePlayer(player_id, 'buyer', budget, product_list)
#         for i in range(number_of_sellers):
#             player_id = 'seller_' + str(i)
#             self.players[player_id] = pl.ConstantPricePlayer(player_id, 'seller', budget, product_list)
#
#
#     def run_simulation(self):
#         pass
#
#     def run_one_step(self):
#         pass
#
#     def print_step_result(self):
#         pass
#
#     def print_end_result(self):
#         pass
#
#     def visualize(self):
#         pass