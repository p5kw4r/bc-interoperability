from web3 import Web3, HTTPProvider
from adapter import Adapter
from config import amount, encoding
import database

blockchain_id = 1
endpoint_uri = 'http://localhost:8545'


class EthAdapter(Adapter):
    credentials = database.get_credentials(blockchain_id)
    address = credentials['address']
    key = credentials['key']
    web3 = Web3(HTTPProvider(endpoint_uri))
    client = web3.eth

    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getTransaction(transaction_hash)

    @staticmethod
    def extract_data(transaction):
        return transaction.input

    @staticmethod
    def to_text(data):
        return Web3.toText(data)

    @classmethod
    def create_transaction(cls, text):
        transaction = {
            'from': cls.address,
            'to': cls.address,
            'gasPrice': cls.client.gasPrice,
            'value': amount,
            'data': bytes(text, encoding=encoding),
            'nonce': cls.get_transaction_count()
        }
        transaction['gas'] = cls.estimate_gas(transaction)
        return transaction

    @classmethod
    def get_transaction_count(cls):
        return cls.client.getTransactionCount(cls.address)

    @classmethod
    def estimate_gas(cls, transaction):
        return cls.client.estimateGas(transaction)

    @classmethod
    def sign_transaction(cls, transaction):
        result = cls.client.account.signTransaction(transaction, cls.key)
        return result.rawTransaction

    @classmethod
    def send_raw_transaction(cls, transaction):
        transaction_hash = cls.client.sendRawTransaction(transaction)
        return transaction_hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, blockchain_id)
