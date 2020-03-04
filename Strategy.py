from abc import abstractmethod


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
