from abc import ABC, abstractmethod

default_amount = 0
encoding = 'utf-8'


class Adapter(ABC):
    @abstractmethod
    def store(self, text):
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, transaction_hash):
        raise NotImplementedError()
