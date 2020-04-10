from abc import abstractmethod
import numpy as np
from sklearn.linear_model import LinearRegression


class CostStrategy:
    def __init__(self):
        pass

    @abstractmethod
    def cost_estimation(self, **kwargs):  # TODO:might change the arguments
        pass


class BidStrategy:

    """
    TODO: Bids are irrelevant, let the agent bid its cost estimation!
    """

    def __init__(self):
        pass

    @abstractmethod
    def winner_determination_function_estimation(self, **kwargs):
        pass

    @abstractmethod
    def bid_strategy(self, **kwargs):
        pass


class NashEquilibriumBidStrategy(BidStrategy):

    def winner_determination_function_estimation(self, **kwargs):
        return 1

    def bid_strategy(self, **kwargs):
        try:
            valuation, type_of_auction = kwargs["valuation"], kwargs["type_of_auction"]
        except:
            raise ValueError("Enter arguments of valuation, type_of_auction")
        if type_of_auction == "first":
            try:
                n = kwargs["number_of_players"]
                return (n / (n + 1)) * valuation
            except:
                raise ValueError("first price auction with no number_of_players argument")
        elif type_of_auction == "second":
            return valuation
        else:
            raise ValueError("auction type parameter was entered illegaly - legal inputs: first/second")


class AggregatedHistoryCostStrategy(CostStrategy):
    def __init__(self):
        super(AggregatedHistoryCostStrategy, self).__init__()

    def cost_estimation(self, **kwargs):
        """
        This function supposed to get a list of product costs and produce an estimation based on predefined aggreagation function
        If  there is no history (i.e. first round) choose an arbitrary cost from [0,v_i] interval.
        :param kwargs:
        :return:
        """
        try:
            aggregation = kwargs["agg"]
            price_history = kwargs["price_history"]
            if not price_history:
                return np.random.randint(0, int(kwargs["evaluaion"]))
            if aggregation == "mean":
                return np.mean(price_history)
            elif aggregation == "median":
                return np.median(price_history)
            elif aggregation == "max":
                return max(price_history)
            elif aggregation == "min":
                return min(price_history)
            elif aggregation == "last":
                return price_history[-1]
            else:
                raise ValueError("Enter history argument to strategy cost estimation function")
        except KeyError:
            raise KeyError("key value error in kwargs - check function arguments")


class LinearRegressionCostStrategty(CostStrategy):
    def __init__(self):
        super(LinearRegressionCostStrategty, self).__init__()

    @staticmethod
    def create_ds(price_history):
        X = []
        y = []
        for i,price in enumerate(price_history):
            if i==0:
                continue
            X.append([price_history[i-1],])
            y.append([price,])
        return np.array(X),np.array(y)

    def cost_estimation(self, **kwargs):
        price_history = kwargs["price_history"]
        if not price_history:
            return np.random.randint(0, int(kwargs["evaluaion"]))

        X,y = self.create_ds(price_history)
        model = LinearRegression().fit(X,y)

        return model.predict(price_history[-1])