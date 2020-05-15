from abc import abstractmethod
import numpy as np


class SellerStrategy:
    def __init__(self):
        pass

    @abstractmethod
    def set_selling_price(self, **kwargs):
        pass


class LinearSellerStrategy(SellerStrategy):
    def __init__(self):
        super().__init__()

    def set_selling_price(self, **kwargs):
        initial_price = kwargs["initial_price"]
        num_of_turn = kwargs["num_of_turn"]
        total_turns = kwargs["total_turns"]
        return initial_price * (total_turns - num_of_turn) / total_turns


class NoisyLinearSellerStrategy(LinearSellerStrategy):

    def __init__(self):
        super().__init__()

    def set_selling_price(self, **kwargs):
        raw_price = super(NoisyLinearSellerStrategy, self).set_selling_price(**kwargs)
        noise = np.random.normal(raw_price, raw_price/10)
        return raw_price + noise


class AdaptiveSellerStrategy(SellerStrategy):
    def __init__(self):
        super().__init__()

    def set_selling_price(self, **kwargs):
        sold_last_turn = kwargs["sold_last_turn"]
        last_price = kwargs["last_price"]
        step = kwargs["step"]
        selling_price = last_price
        if not sold_last_turn:
            selling_price -= step
        return selling_price


class NoisyAdaptiveSellerStrategy(AdaptiveSellerStrategy):

    def __init__(self):
        super().__init__()

    def set_selling_price(self, **kwargs):
        raw_price = super(NoisyAdaptiveSellerStrategy, self).set_selling_price(**kwargs)
        noise = np.random.normal(raw_price, raw_price/10)
        return raw_price + noise


# class MarketPriceStrategy(SellerStrategy):
#
#     def __init__(self):
#         super().__init__()
#
#     def set_selling_price(self, **kwargs):
#         pass
