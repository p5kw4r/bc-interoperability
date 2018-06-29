from web3 import Web3, HTTPProvider
from adapter import Adapter
from config import amount, encoding

endpoint_uri = 'http://localhost:8545'

web3 = Web3(HTTPProvider(endpoint_uri))
client = web3.eth

address = '0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe'
key = 'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'


class EthAdapter(Adapter):
    @staticmethod
    def get_transaction(transaction_hash):
        return client.getTransaction(transaction_hash)

    @staticmethod
    def extract_data(transaction):
        return transaction.input

    @staticmethod
    def to_text(data):
        return Web3.toText(data)

    @staticmethod
    def get_transaction_count():
        return client.getTransactionCount(address)

    @classmethod
    def create_transaction(cls, text):
        data = bytes(text, encoding=encoding)
        transaction = {
            'from': address,
            'to': address,
            'gasPrice': client.gasPrice,
            'value': amount,
            'data': data,
            'nonce': cls.get_transaction_count()
        }
        transaction['gas'] = cls.estimate_gas(transaction)
        return transaction

    @staticmethod
    def estimate_gas(transaction):
        return client.estimateGas(transaction)

    @staticmethod
    def sign_transaction(transaction):
        result = client.account.signTransaction(transaction, key)
        return result.rawTransaction

    @staticmethod
    def send_raw_transaction(transaction):
        transaction_hash = client.sendRawTransaction(transaction)
        return transaction_hash
