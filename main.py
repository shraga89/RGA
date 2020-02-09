from config import *
from utils import *
import Player
import Simulation


def main():
    # players = generate_players()
    # for player in players.values():
    #     print(player)
    my_sim = Simulation.UniformBudgetSimulation(1, 1, 0, 10, 1000, ["oil"])
    my_sim.run_simulation()


if __name__ == '__main__':
    main()