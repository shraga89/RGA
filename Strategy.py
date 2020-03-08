from abc import abstractmethod
import numpy as np

class Strategy:
    def __init__(self):
        pass

    @abstractmethod
    def bid_strategy(self, **kwargs):
        pass

    @abstractmethod
    def cost_estimation(self, **kwargs):  # TODO:might change the arguments
        pass

    @abstractmethod
    def winner_determination_function_estimation(self, **kwargs):
        pass


class ConservativeStrategy(Strategy):

    def __init__(self):
        super(ConservativeStrategy, self).__init__()

    def bid_strategy(self, **kwargs):
        try:
            valuation = kwargs["valuation"]
            return valuation
        except:
            raise ValueError("Enter valuation argument")

    def cost_estimation(self, **kwargs):
        try:
            valuation = kwargs["valuation"]
            return valuation
        except:
            raise ValueError("Enter valuation argument")

    def winner_determination_function_estimation(self, **kwargs):
        return 1


class AuctionAwareConservativeStrategy(Strategy):

    def __init__(self):
        super(AuctionAwareConservativeStrategy, self).__init__()

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

    def cost_estimation(self, **kwargs):
        try:
            valuation = kwargs["valuation"]
            return valuation
        except:
            raise ValueError("Enter valuation argument")

    def winner_determination_function_estimation(self, **kwargs):
        return 1


class NaiveHistoryBasedStrategy(Strategy):
    def __init__(self):
        super(NaiveHistoryBasedStrategy,self).__init__()

    def winner_determination_function_estimation(self, **kwargs):
        return 1

class AggregatedHistory(NaiveHistoryBasedStrategy):
    def __init__(self):
        super(AggregatedHistory,self).__init__()

    def cost_estimation(self, **kwargs):
        """
        This function supposed to get a list of product costs and produce an estimation based on predefined aggreagation function
        If  there is no history (i.e. first round) choose an arbitrary cost from [0,v_i] interval.
        :param kwargs:
        :return:
        """
        try:
            aggregation = kwargs["agg"]
            history = kwargs["history"]
            if not history:
                return np.random.randint(0,int(kwargs["evaluaion"]))
            if aggregation=="mean":
                return np.mean(history)
            elif aggregation=="median":
                return np.median(history)
            elif aggregation=="max":
                return max(history)
            elif aggregation=="min":
                return min(history)
            elif aggregation=="last":
                return history[-1]
            else:
                raise ValueError("Enter history argument to strategy cost estimation function")
        except KeyError:
            raise KeyError("Enter history argument to strategy cost estimation function")


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

