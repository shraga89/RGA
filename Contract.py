from abc import abstractmethod
import operator


class Contract:

    def __init__(self):
        pass

    @abstractmethod
    def check_prerequisites(self, stakeholders: list, product):
        pass

    @abstractmethod
    def enact_contact(self, stakeholders: list, product):
        pass


class SimpleSellingContract(Contract):

    def __init__(self):
        super().__init__()

    def check_prerequisites(self, stakeholders, product):
        seller, buyer = stakeholders[0], stakeholders[1]
        actual_price = seller.get_current_selling_price(product)
        if actual_price > buyer.get_current_buying_price(product):
            return False, 'unsuccessful'
        elif actual_price > buyer.budget:
            return False, 'no budget'
        else:
            return True, 'successful'

    def enact_contact(self, stakeholders: list, product):
        seller, buyer = stakeholders[0], stakeholders[1]
        actual_price = seller.get_current_selling_price(product)
        buyer.add_inventory(product, 1)
        seller.budget += actual_price
        buyer.budget -= actual_price
        return actual_price


class Auction:

    def __init__(self):
        pass

    def run_auction(self, bids, **kwargs):
        winner = self.winner_determination(bids, **kwargs)
        prices = self.price_determination(bids, **kwargs)
        return winner, prices

    @abstractmethod
    def winner_determination(self, bids, **kwargs):
        pass

    @abstractmethod
    def price_determination(self, bids, **kwargs):
        pass


class FirstPriceAuction(Auction):

    def __init__(self):
        super().__init__()

    def winner_determination(self, bids, **kwargs):
        return max(bids.items(), key=operator.itemgetter(1))[0]

    def price_determination(self, bids, **kwargs):
        return max(bids.items(), key=operator.itemgetter(1))[1]


class SecondPriceAuction(Auction):

    def __init__(self):
        super().__init__()

    def winner_determination(self, bids, **kwargs):
        if not bids:
            return None
        threshold_price = kwargs.get("threshold_price", 0)
        winner = max(bids.items(), key=operator.itemgetter(1))[0]
        if bids[winner] >= threshold_price:
            return winner
        else:
            return None

    def price_determination(self, bids, **kwargs):
        winner = self.winner_determination(bids, **kwargs)
        if winner is None:
            return None
        threshold_price = kwargs.get("threshold_price", 0)
        if len(bids) == 1:
            return threshold_price
        second_place_player = sorted(bids.keys(), key=lambda x: (bids[x], x), reverse=True)[1]
        price_candidate = bids[second_place_player]
        if price_candidate >= threshold_price:
            return price_candidate
        else:
            return threshold_price


if __name__=="__main__":
    my_auction = SecondPriceAuction()
    # bids = {"greg":3, "alex":2,'shraga':1}
    bids = {}
    print(my_auction.run_auction(bids, threshold_price = 1.5))