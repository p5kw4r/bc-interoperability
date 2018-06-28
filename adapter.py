from abc import ABC, abstractmethod

default_amount = 0
encoding = 'utf-8'


class Adapter(ABC):
    @classmethod
    @abstractmethod
    def store(cls, text):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def retrieve(cls, tx_hash):
        raise NotImplementedError()
