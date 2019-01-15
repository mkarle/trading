from abc import ABCMeta, abstractmethod
import pandas as pd


EMPTY = '---'
BUY = 'BUY'
SELL = 'SELL'


class Transaction(metaclass=ABCMeta):
    CATEGORIES = [EMPTY, BUY, SELL]

    def __init__(self, quantity=0, transaction=EMPTY, price=0.0):
        self.quantity = quantity
        self.transaction = transaction
        self.price = price

    def __str__(self):
        return '{} {} {}'.format(self.transaction, self.quantity, self.price)
    '''
        Returns returns the quantity * price
    '''
    @abstractmethod
    def get_total_price(self):
        return

    @abstractmethod
    def get_effect_on_quantity(self):
        return


class EmptyTransaction(Transaction):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return self.transaction

    def get_effect_on_quantity(self):
        return 0

    def get_total_price(self):
        return 0


class BuyTransaction(Transaction):

    def __init__(self, quantity=0, price=0.0):
        super().__init__(quantity=quantity, transaction=BUY, price=price)

    def get_effect_on_quantity(self):
        return self.quantity

    def get_total_price(self):
        return - self.quantity * self.price


class SellTransaction(Transaction):

    def __init__(self, quantity=0, price=0.0):
        super().__init__(quantity=quantity, price=price, transaction=SELL)

    def get_effect_on_quantity(self):
        return - 1 * self.quantity

    def get_total_price(self):
        return self.quantity * self.price


def initialize_actions(dates, symbols):
    return pd.DataFrame(EmptyTransaction(), index=dates, columns=symbols)
