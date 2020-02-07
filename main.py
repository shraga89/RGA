from config import *
from utils import *
import Player


def main():
    players = generate_players()
    for player in players.values():
        print(player)


if __name__ == '__main__':
    main()