from config import *
import Player as P


def generate_players():
    players = {}
    for i in range(sellers_number):
        player_id = 'seller_' + str(i)
        players[player_id] = P.Player(player_id, 'seller', 100, ['oil'])
    for i in range(buyers_number):
        player_id = 'buyer_' + str(i)
        players[player_id] = P.Player(player_id, 'buyer', 100, ['oil'])
    return players
