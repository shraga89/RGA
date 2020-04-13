from config import *
# from Player import DataConsumer
from scipy import stats as st
from BuyerStrategy import AggregatedHistoryCostStrategy
from gurobipy import Model, GRB, quicksum
from Utility import *


class ExtendedKnapsack:
    def __init__(self, player, products, distribution: str):
        self.player = player
        self.products = products
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

    def __init__(self, player, products, distribution: str = "uniform"):
        super().__init__(player, products, distribution)

    def solve(self, turn, total_steps, costs) -> set:

        model = Model()
        products = self.products
        budget = self.player.budget
        print(budget)
        valuations = self.player.product_values_for_player
        # costs, _, bids = self.player.get_estimations_for_optimization(turn=turn, total_steps=total_steps)

        x = {}
        for product in products:
            x[product] = model.addVar(vtype=GRB.BINARY)
            # print(x[product], valuations[product], costs[product])

        model.setObjective(quicksum(x[product] * (valuations[product] - costs[product]) for product in products),
                           GRB.MAXIMIZE)
        model.addConstr(quicksum(x[product] * costs[product] for product in products) <= budget)

        model.optimize()

        to_return = set()
        for product, variable in x.items():
            if x[product].x > 0:
                to_return.add(product)

        return to_return


if __name__ == '__main__':
    pass
    # my_player = DataConsumer("greg", 10000, ["a", "b", "c"], ["a", "b", "c"], {"a": 30, "b": 40, "c": 50},
    #                          SimpleDataPlayerUtility(),7)
    # my_player.set_cost_estimation_strategy(AggregatedHistoryCostStrategy())
    # my_solver = NaiveKnapsack(my_player, "dist")
    # print(my_solver.solve(1,7,{"a":2,"b":3}))
