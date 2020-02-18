from config import *
from utils import *
import Player
import Simulation
import Contract


# TODO: update run_one_step_for_single_product in ProductionConsumptionSimulation
# TODO: consider changing the history
# TODO: update set_current_prices and remember to address the inventory


def main():
    # my_players = generate_players(pl.RationalPlayer, SELLERS_NUMBER,
    #                               BUYERS_NUMBER, VERSATILES_NUMBER, 2000, PRODUCTS_LIST)
    # my_players = generate_players(pl.NaiveProductionConsumptionPlayer, SELLERS_NUMBER,
    #                               BUYERS_NUMBER, VERSATILES_NUMBER, MINIMAL_BUYING_BUDGET,
    #                               MAXIMAL_BUYING_BUDGET, MINIMAL_SELLING_BUDGET, MAXIMAL_SELLING_BUDGET,
    #                               CONSTANT_PRODUCTION_PRICE, PRODUCTS_LIST)
    my_products = generate_data_products(NUMBER_OF_PRODUCTS, MINIMAL_NUMBER_OF_EXAMPLES,
                                         MAXIMAL_NUMBER_OF_EXAMPLES, MINIMAL_NUMBER_OF_FEATURES,
                                         MAXIMAL_NUMBER_OF_FEATURES)
    my_players = generate_data_players(BUYERS_NUMBER, SELLERS_NUMBER, MINIMAL_BUYING_BUDGET,
                                       MAXIMAL_BUYING_BUDGET, MINIMAL_SELLING_BUDGET, MAXIMAL_SELLING_BUDGET,
                                       CONSTANT_PRODUCTION_PRICE, CONSTANT_CONSUMPTION_UTILITY,
                                       NUMBER_OF_PRODUCTS_PER_BUYER, NUMBER_OF_PRODUCTS_PER_SELLER,
                                       my_products)
    for player in my_players.values():
        print(player)
        print('----')
    contract = Contract.SimpleSellingContract()
    my_sim = Simulation.DataMarketSimulation(TIME_HORIZON, PRODUCTS_LIST, my_players, contract)
    my_sim.run_simulation()


if __name__ == '__main__':
    main()
