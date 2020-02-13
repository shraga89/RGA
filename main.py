from config import *
from utils import *
import Player
import Simulation

# TODO: update run_one_step_for_single_product in ProductionConsumptionSimulation
# TODO: consider changing the history
# TODO: update set_current_prices and remember to address the inventory


def main():
    # my_players = generate_players(pl.RationalPlayer, SELLERS_NUMBER,
    #                               BUYERS_NUMBER, VERSATILES_NUMBER, 2000, PRODUCTS_LIST)
    my_players = generate_players(pl.NaiveProductionConsumptionPlayer, SELLERS_NUMBER,
                                  BUYERS_NUMBER, VERSATILES_NUMBER, MINIMAL_BUYING_BUDGET,
                                  MAXIMAL_BUYING_BUDGET, MINIMAL_SELLING_BUDGET, MAXIMAL_SELLING_BUDGET,
                                  CONSTANT_PRODUCTION_PRICE, PRODUCTS_LIST)
    for player in my_players.values():
        print(player)
        print('----')
    # my_sim = Simulation.NaiveSimulation(TIME_HORIZON, PRODUCTS_LIST, my_players)
    # my_sim.run_simulation()


if __name__ == '__main__':
    main()
