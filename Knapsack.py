from config import *
from Player import DataConsumer
from scipy import stats as st
from Strategy import ConservativeStrategy
from gurobipy import *
from Utility import *


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


class NaiveKnapsack(ExtendedKnapsack):

    def __init__(self, player: DataConsumer, distribution: str):
        super().__init__(player, distribution)

    def solve(self):

        model = Model()
        products = self.products
        budget = self.player.budget
        valuations = self.player.product_values_for_player
        costs, _, _ = self.player.get_estimations_for_optimization(**{"turn": 6, "total_steps": 100})

        n = len(products)
        x = {}
        for product in products:
            x[product] = model.addVar(n, vtype=GRB.BINARY, name='x')
            print(x[product], valuations[product], costs[product])

        model.setObjective(quicksum(x[product] * valuations[product] for product in products), GRB.MAXIMIZE)
        model.addConstr(quicksum(x[product] * costs[product]) <= budget for product in products)

        model.optimize()


if __name__ == '__main__':
    my_player = DataConsumer("greg", 1000, ["a", "b", "c"], ["a", "b", "c"], {"a": 30, "b": 40, "c": 50},
                             SimpleDataPlayerUtility())
    my_player.set_strategy(ConservativeStrategy())
    my_solver = NaiveKnapsack(my_player, "dist")
    my_solver.solve()





