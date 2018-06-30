from web3 import Web3, HTTPProvider
from adapter import Adapter
from config import amount, encoding

endpoint_uri = 'http://localhost:8545'

address = '0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe'
key = 'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'


class EthAdapter(Adapter):
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
    def get_transaction_count(cls):
        return cls.client.getTransactionCount(address)

    @classmethod
    def create_transaction(cls, text):
        transaction = {
            'from': address,
            'to': address,
            'gasPrice': cls.client.gasPrice,
            'value': amount,
            'data': bytes(text, encoding=encoding),
            'nonce': cls.get_transaction_count()
        }
        transaction['gas'] = cls.estimate_gas(transaction)
        return transaction

    @classmethod
    def estimate_gas(cls, transaction):
        return cls.client.estimateGas(transaction)

    @classmethod
    def sign_transaction(cls, transaction):
        result = cls.client.account.signTransaction(transaction, key)
        return result.rawTransaction

    @classmethod
    def send_raw_transaction(cls, transaction):
        transaction_hash = cls.client.sendRawTransaction(transaction)
        return transaction_hash
