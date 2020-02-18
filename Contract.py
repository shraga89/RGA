from abc import abstractmethod


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
