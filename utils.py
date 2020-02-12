from config import *
import Player as pl


def generate_players(players_type, number_of_buyers, number_of_sellers, number_of_versatile_players, budget, product_list):
    players = {'buyers': {}, 'sellers': {}}
    for i in range(number_of_buyers):
        player_id = 'buyer_' + str(i)
        new_player = players_type(player_id, 'buyer', budget, product_list)
        players['buyers'][player_id] = new_player
    for i in range(number_of_sellers):
        player_id = 'seller_' + str(i)
        new_player = players_type(player_id, 'seller', budget, product_list)
        players['sellers'][player_id] = new_player
    for i in range(number_of_versatile_players):
        player_id = 'versatile_' + str(i)
        new_player = players_type(player_id, 'versatile', budget, product_list)
        players['buyers'][player_id] = new_player
        players['sellers'][player_id] = new_player
    return players