from config import *
import Player as pl


def generate_players():
    players = {}
    for i in range(SELLERS_NUMBER):
        player_id = 'seller_' + str(i)
        players[player_id] = pl.ConstantPricePlayer(player_id, 'seller', 100, ['oil'])
    for i in range(BUYERS_NUMBER):
        player_id = 'buyer_' + str(i)
        players[player_id] = pl.ConstantPricePlayer(player_id, 'buyer', 100, ['oil'])
    return players
