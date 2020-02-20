from abc import abstractmethod


class AbstractUtility:

    def __init__(self, algorithm_ratio=1, budget_ratio=1):
        self.algorithm_ratio = algorithm_ratio
        self.budget_ratio = budget_ratio

    @abstractmethod
    def calculate_algorithms_utility(self, player_value_for_products: dict, product_turn_bought: dict,
                                     owned_products: list,
                                     turn):
        pass

    def calculate_budget_utility(self, budget):  # TODO: maybe make it return budget - discuss further functionality
        pass

    def calculate_total_utility(self, algorithm_utility, budget):
        """
        method that returns player's total utility at current turn. tradeoff parameter will allow to model external noises
        in a players utility (not effected solely by profit).
        :return:
        """
        return self.algorithm_ratio * algorithm_utility + self.budget_ratio * budget


# class SimpleUtility(AbstractUtility):
#     """
#     Class defines utility as the sum of product values to the player minus the total products cost.
#     In addition, we add the current seller budget that player has
#     """
#
#     def __init__(self):
#         super(SimpleUtility, self).__init__()
#
#     def calculate_buyer_utility(self, player_value_for_products: dict, owned_products: list):
#         return sum([player_value_for_products[product] for product in owned_products])
#
#     def calculate_seller_utility(self, budget):
#         return budget


# class LeverageUtility(AbstractUtility):
#     """
#     Class defines utility of buyer as the sum of product values to the player minus the total products cost.
#     Product values are also a function of the number of player that own the products.
#     In addition, we add the current seller budget that player has
#     """
#     current_product_owners = dict()  # class shared object for knowing the possession of products
#
#     def __init__(self, number_of_players):
#         super(LeverageUtility, self).__init__()
#         self.number_of_players = number_of_players
#
#     def real_value_of_player(self, player_raw_value, product):
#         number_of_owners = len(self.current_product_owners[product])
#         return player_raw_value * ((self.number_of_players - number_of_owners) / self.number_of_players)
#
#     def calculate_buyer_utility(self, player_value_for_products: dict, owned_products: list):
#         return sum(
#             [self.real_value_of_player(player_value_for_products[product], product) for
#              product in owned_products])
#
#     def calculate_seller_utility(self, budget):
#         return budget


class DataPlayerUtility(AbstractUtility):
    """
    Class for data player utility calculations.
    Player's utility is based on the time the datasets are in his custody and the number of players sharing the data.
    In addition, we add the budget of the player.
    Currently, each dataset means a single algorithm is used w.r.t. him - might be changed on future.
    """
    current_product_owners = dict()  # class shared object for knowing the possession of products

    def __init__(self, number_of_players, decay_factor=1, algorithm_ratio=1, budget_ratio=1):
        super(DataPlayerUtility, self).__init__(algorithm_ratio, budget_ratio)
        self.number_of_players = number_of_players
        self.decay_factor = decay_factor

    def update_product_owners(self, product, player):
        if product not in self.current_product_owners:
            self.current_product_owners[product] = []
        self.current_product_owners[product].append(player)

    # TODO: change number of player to number of players eligible for dataset
    def calculate_algorithms_utility(self, player_value_for_products: dict, product_turn_bought: dict,
                                     owned_products: list,
                                     turn):
        algorithms_utility = {}
        for product in owned_products:
            player_raw_value = player_value_for_products[product]
            time_based_utility = player_raw_value * self.decay_factor ** (turn - product_turn_bought[product])
            number_of_product_owners = len(self.current_product_owners[product])
            shared_product_utility = player_raw_value * (
                    (self.number_of_players - number_of_product_owners) / self.number_of_players)
            algorithms_utility[product] = (time_based_utility + shared_product_utility) / 2
        return algorithms_utility

    def calculate_budget_utility(self, budget):
        return budget
