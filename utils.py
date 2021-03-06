import Player as pl
import random
import Product as pr
import os,shutil
from BuyerStrategy import NashEquilibriumBidStrategy, AggregatedHistoryCostStrategy, LinearRegressionCostStrategty
from SellerStrategy import AdaptiveSellerStrategy,LinearSellerStrategy,NoisyAdaptiveSellerStrategy,NoisyLinearSellerStrategy

def set_initial_production_price(products, constant_production_price):
    initial_production_prices = dict()
    for product in products:
        initial_production_prices[product] = constant_production_price
    return initial_production_prices


def set_initial_consumption_utility(products, constant_consumption_utility):
    initial_consumption_utilities = dict()
    for product in products:
        initial_consumption_utilities[product] = constant_consumption_utility
    return initial_consumption_utilities


def set_threshold_values(relevant_products, minimum_threshold_value, maximum_threshold_value):
    return {product: random.randint(minimum_threshold_value, maximum_threshold_value) for product in relevant_products}


def generate_random_budget(minimal_budget, maximal_budget):
    return random.randint(minimal_budget, maximal_budget)


def generate_players(players_type, number_of_buyers, number_of_sellers,
                     number_of_versatile_players, minimal_buying_budget, maximal_buying_budget,
                     minimal_selling_budget, maximal_selling_budget, constant_production_price,
                     constant_consumption_utility, product_list):
    players = {'buyers': {}, 'sellers': {}}
    for i in range(number_of_buyers):
        player_id = 'buyer_' + str(i)
        budget = generate_random_budget(minimal_buying_budget, maximal_buying_budget)
        initial_consumption_utility = set_initial_consumption_utility(product_list, constant_consumption_utility)
        new_player = players_type(player_id, 'buyer', budget, product_list, None, initial_consumption_utility)
        players['buyers'][player_id] = new_player
    for i in range(number_of_sellers):
        player_id = 'seller_' + str(i)
        budget = generate_random_budget(minimal_selling_budget, maximal_selling_budget)
        initial_production_price = set_initial_production_price(product_list, constant_production_price)
        new_player = players_type(player_id, 'seller', budget, product_list, initial_production_price, None)
        players['sellers'][player_id] = new_player
    for i in range(number_of_versatile_players):
        player_id = 'versatile_' + str(i)
        budget = generate_random_budget(minimal_selling_budget, maximal_selling_budget)
        new_player = players_type(player_id, 'versatile', budget, product_list, None, None)
        players['buyers'][player_id] = new_player
        players['sellers'][player_id] = new_player
    return players


# def generate_data_players(number_of_buyers, number_of_sellers, minimal_buying_budget, maximal_buying_budget,
#                           minimal_selling_budget, maximal_selling_budget, constant_production_price,
#                           constant_consumption_utility, number_of_products_per_buyer, number_of_products_per_seller,
#                           product_list, decay_factor, minimal_selling_price, maximal_selling_price,horizon):
#     players = {'buyers': {}, 'sellers': {}}
#     for i in range(number_of_buyers):
#         # cost_estimation_strategy = AggregatedHistoryCostStrategy()
#         cost_estimation_strategy = LinearRegressionCostStrategty()
#         bid_strategy = NashEquilibriumBidStrategy()
#         player_id = 'buyer_' + str(i)
#         budget = generate_random_budget(minimal_buying_budget, maximal_buying_budget)
#         initial_consumption_utility = set_initial_consumption_utility(product_list, constant_consumption_utility)
#         new_player = pl.DataConsumer(player_id, budget, product_list, initial_consumption_utility,
#                                      horizon)
#
#         new_player.set_cost_estimation_strategy(cost_estimation_strategy)
#         new_player.set_bid_strategy(bid_strategy)
#
#         players['buyers'][player_id] = new_player
#     for i in range(number_of_sellers):
#         player_id = 'seller_' + str(i)
#         budget = generate_random_budget(minimal_selling_budget, maximal_selling_budget)
#         initial_production_price = set_initial_production_price(product_list, constant_production_price)
#         relevant_products = random.sample(product_list, number_of_products_per_seller)
#         threshold_values = set_threshold_values(relevant_products, minimal_selling_price, maximal_selling_price)
#         new_player = pl.DataProvider(player_id, budget, product_list, relevant_products, initianl_production_price,
#                                      threshold_values,horizon)
#         players['sellers'][player_id] = new_player
#     return players

def generate_valuations(number_of_buyers,product_list,min_valuation,max_valuation):
    valutions_list = []
    for i in range(number_of_buyers):
        valuations = {p:random.randint(min_valuation,max_valuation) for p in product_list}
        valutions_list.append(valuations)
    return valutions_list

def assign_valuations_to_buyers(buyers,valutions_list,offset):
    for i,buyer in enumerate(buyers):
        buyers[buyer].set_valuations(valutions_list[(i+offset)%len(valutions_list)])

def generate_buyers(budget,product_list,horizon,players,types_of_buyers):

    for i,type in enumerate(types_of_buyers):
        cost_estimation_strategy = type
        player_id = 'buyer_' + str(i)
        new_player = pl.DataConsumer(player_id, budget, product_list,horizon)

        new_player.set_cost_estimation_strategy(cost_estimation_strategy)
        players['buyers'][player_id] = new_player

def generate_sellers(product_list,number_of_products_per_seller,horizon,players):
    types_of_sellers = [LinearSellerStrategy(),AdaptiveSellerStrategy(),NoisyLinearSellerStrategy(),NoisyAdaptiveSellerStrategy()]*2
    # types_of_sellers = [AdaptiveSellerStrategy(),]*10
    # types_of_sellers = [LinearSellerStrategy(),AdaptiveSellerStrategy(),NoisyLinearSellerStrategy()]*3
    for i,type in enumerate(types_of_sellers):
        player_id = 'seller_' + str(i)
        relevant_products = random.sample(product_list, number_of_products_per_seller)
        new_player = pl.DataProvider(player_id, product_list, relevant_products,horizon)
        new_player.set_selling_strategy(type)
        players['sellers'][player_id] = new_player


def generate_data_products(number_of_products, minimal_number_of_examples,
                           maxmal_number_of_examples, minimal_number_of_features,
                           maxmal_number_of_features):
    product_list = []
    for p in range(number_of_products):
        product_name = 'product_' + str(p)
        domain = 'general'
        number_of_examples = random.randint(minimal_number_of_examples, maxmal_number_of_examples)
        number_of_features = random.randint(minimal_number_of_features, maxmal_number_of_features)
        additional_features = None
        new_product = pr.DataProduct(product_name, domain, number_of_examples, number_of_features, additional_features)
        product_list.append(new_product)
    return product_list

def clear_old_results(results_folder):
    if os.path.exists(results_folder):
        shutil.rmtree(results_folder, ignore_errors=True)