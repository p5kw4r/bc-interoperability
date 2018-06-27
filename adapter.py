from abc import ABC, abstractmethod


class Adapter(ABC):
    @abstractmethod
    def store(self, text):
        raise NotImplementedError()

    @abstractmethod
    def retrieve(self, transaction_hash):
        raise NotImplementedError()
