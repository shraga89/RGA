from config import *
from utils import *
import Player
import Simulation


def main():
    # players = generate_players()
    # for player in players.values():
    #     print(player)
    my_players = generate_players(pl.RationalPlayer, SELLERS_NUMBER,
                                  BUYERS_NUMBER, VERSATILES_NUMBER, 2000, PRODUCTS_LIST)
    for player in my_players.values():
        print(player)
        print('----')
    my_sim = Simulation.UniformBudgetSimulation(TIME_HORIZON, PRODUCTS_LIST, my_players)
    my_sim.run_simulation()


if __name__ == '__main__':
    main()
