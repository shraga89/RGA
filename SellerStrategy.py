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
        initial_price = kwargs["initial price"]
        num_of_turn = kwargs["num of turn"]
        total_turns = kwargs["total turns"]
        return initial_price * (total_turns - num_of_turn) / total_turns


class AdaptiveSellerStrategy(SellerStrategy):
    def __init__(self):
        super().__init__()

    def set_selling_price(self, **kwargs):
        sold_last_turn = kwargs["sold last turn"]
        last_price = kwargs["last price"]
        step = kwargs["step"]
        selling_price = last_price
        if not sold_last_turn:
            selling_price -= step
        return selling_price

