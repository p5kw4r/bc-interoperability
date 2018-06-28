from abc import ABC, abstractmethod

default_amount = 0
encoding = 'utf-8'


class Adapter(ABC):
    @staticmethod
    @abstractmethod
    def store(text):
        raise NotImplementedError()

    @staticmethod
    @abstractmethod
    def retrieve(transaction_hash):
        raise NotImplementedError()
