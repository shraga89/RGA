from config import *
from utils import *
import Simulation
import Contract




def main():
    # my_players = generate_players(pl.RationalPlayer, SELLERS_NUMBER,
    #                               BUYERS_NUMBER, VERSATILES_NUMBER, 2000, PRODUCTS_LIST)
    # my_players = generate_players(pl.NaiveProductionConsumptionPlayer, SELLERS_NUMBER,
    #                               BUYERS_NUMBER, VERSATILES_NUMBER, MINIMAL_BUYING_BUDGET,
    #                               MAXIMAL_BUYING_BUDGET, MINIMAL_SELLING_BUDGET, MAXIMAL_SELLING_BUDGET,
    #                               CONSTANT_PRODUCTION_PRICE, PRODUCTS_LIST)
    products_list = generate_data_products(NUMBER_OF_PRODUCTS, MINIMAL_NUMBER_OF_EXAMPLES,
                                           MAXIMAL_NUMBER_OF_EXAMPLES, MINIMAL_NUMBER_OF_FEATURES,
                                           MAXIMAL_NUMBER_OF_FEATURES)
    players = generate_data_players(BUYERS_NUMBER, SELLERS_NUMBER, MINIMAL_BUYING_BUDGET,
                                    MAXIMAL_BUYING_BUDGET, MINIMAL_SELLING_BUDGET, MAXIMAL_SELLING_BUDGET,
                                    CONSTANT_PRODUCTION_PRICE, CONSTANT_CONSUMPTION_UTILITY,
                                    NUMBER_OF_PRODUCTS_PER_BUYER, NUMBER_OF_PRODUCTS_PER_SELLER,
                                    products_list, DECAY_FACTOR, MINIMAL_SELLING_PRICE, MAXIMAL_SELLING_PRICE)
    for player in players.values():
        print(player)
        print('----')
    contract = Contract.SecondPriceAuction()
    my_sim = Simulation.DataMarketSimulation(TIME_HORIZON, products_list, players, contract)
    my_sim.run_simulation()


if __name__ == '__main__':
    main()
