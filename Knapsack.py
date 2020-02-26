from config import *
from Player import DataConsumer
from scipy import stats as st


class ExtendedKnapsack:
    def __init__(self, player: DataConsumer, distribution: str):
        self.player = player
        self.products = player.relevant_products
        self.price_distribution = {}
        for product in self.products:
            self.price_distribution[product] = self.create_distribution(product, distribution)

    def create_distribution(self, product, distribution: str):
        to_return = None
        parameters = self.estimate_parameters(product, distribution)
        if "uniform" in distribution:
            to_return = st.uniform(*parameters)
        return to_return

    def estimate_parameters(self, product, distribution: str):
        if "uniform" in distribution:
            upper_limit = self.player.price_limits[(product, "buying_price")]
            lower_limit = MINIMAL_BUYING_PRICE
            return [lower_limit, upper_limit - lower_limit]
        return None

    def solve(self):
        pass

    def print_out(self):
        pass


class NaiveKnapsacks(ExtendedKnapsack):

    def __init__(self):
        super().__init__()
