from abc import abstractmethod
from typing import Dict


class AbstractUtility:
    utility_stats: Dict[int, list] = dict()  # class shared object for later on possible statistics

    # TODO: maybe make the generic tradeoff even more generic
    def __init__(self, generic_tradeoff_ratio):
        self.generic_tradeoff_ratio = generic_tradeoff_ratio

    @abstractmethod
    def calculate_buyer_utility(self, player_value_for_products: dict, cost_of_product: dict, owned_products: list):
        pass

    @abstractmethod
    def calculate_seller_utility(self, budget):  # TODO: maybe make it return budget - discuss further functionality
        pass

    def calculate_total_utility(self, turn, player_value_for_products: dict, cost_of_product: dict,
                                owned_products: list, budget: int):
        """
        method that returns player's total utility at current turn. tradeoff parameter will allow to model external noises
        in a players utility (not effected solely by profit).
        :return:
        """
        ratio = self.generic_tradeoff_ratio
        current_utility = ratio * self.calculate_seller_utility(budget) + (1 - ratio) * self.calculate_buyer_utility(
            player_value_for_products, cost_of_product, owned_products)
        if turn not in self.utility_stats:
            self.utility_stats[turn] = []
        self.utility_stats[turn].append(current_utility)
        return current_utility


class SimpleUtility(AbstractUtility):
    """
    Class defines utility as the sum of product values to the player minus the total products cost.
    In addition, we add the current seller budget that player has
    """

    def __init__(self, generic_tradeoff_ratio):
        super(SimpleUtility, self).__init__(generic_tradeoff_ratio)

    def calculate_buyer_utility(self, player_value_for_products: dict, cost_of_product: dict, owned_products: list):
        return sum([player_value_for_products[product] - cost_of_product[product] for product in owned_products])

    def calculate_seller_utility(self, budget):
        return budget


class LeverageUtility(AbstractUtility):
    """
    Class defines utility of buyer as the sum of product values to the player minus the total products cost.
    Product values are also a function of the number of player that own the products.
    In addition, we add the current seller budget that player has
    """
    current_product_owners = dict()  # class shared object for knowing the possession of products

    def __init__(self, generic_tradeoff_ratio, number_of_players):
        super(LeverageUtility, self).__init__(generic_tradeoff_ratio)
        self.number_of_players = number_of_players

    def real_value_of_player(self, player_raw_value, product):
        number_of_owners = len(self.current_product_owners[product])
        return player_raw_value * ((self.number_of_players - number_of_owners) / self.number_of_players)

    def calculate_buyer_utility(self, player_value_for_products: dict, cost_of_product: dict, owned_products: list):
        return sum(
            [self.real_value_of_player(player_value_for_products[product], product) - cost_of_product[product] for
             product in owned_products])

    def calculate_seller_utility(self, budget):
        return budget
