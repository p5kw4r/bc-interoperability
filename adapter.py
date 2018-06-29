from abc import ABC, abstractmethod


class Adapter(ABC):
    @property
    @abstractmethod
    def client(self):
        raise NotImplementedError

    @classmethod
    def retrieve(cls, transaction_hash):
        transaction = cls.get_transaction(transaction_hash)
        data = cls.extract_data(transaction)
        return cls.to_text(data)

    @classmethod
    @abstractmethod
    def get_transaction(cls, transaction_hash):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def extract_data(transaction):
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def to_text(data):
        raise NotImplementedError

    @classmethod
    def store(cls, text):
        transaction = cls.create_transaction(text)
        signed_transaction = cls.sign_transaction(transaction)
        transaction_hash = cls.send_raw_transaction(signed_transaction)
        return transaction_hash

    @staticmethod
    @abstractmethod
    def create_transaction(text):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def sign_transaction(cls, transaction):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def send_raw_transaction(cls, transaction):
        raise NotImplementedError
