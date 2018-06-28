from web3 import Web3, HTTPProvider
from adapter import Adapter, default_amount, encoding

endpoint_uri = 'http://localhost:8545'

web3 = Web3(HTTPProvider(endpoint_uri))
client = web3.eth

default_address = '0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe'
private_key = \
    'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'

gas_limit = 90000


class EthAdapter(Adapter):
    @classmethod
    def retrieve(cls, tx_hash):
        tx = cls.get_transaction(tx_hash)
        text = cls.to_text(tx.input)
        return text

    @staticmethod
    def get_transaction(tx_hash):
        tx = client.getTransaction(tx_hash)
        return tx

    @staticmethod
    def to_text(data):
        text = Web3.toText(data)
        return text

    @classmethod
    def store(cls, text):
        data = bytes(text, encoding=encoding)
        tx = cls.create_transaction(data)
        signed_tx = cls.sign_transaction(tx)
        tx_hash = cls.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash

    @staticmethod
    def create_transaction(
            data,
            sender=default_address,
            recipient=default_address,
            gas=gas_limit,
            gas_price=client.gasPrice,
            value=default_amount,
            nonce=client.getTransactionCount(default_address)):
        tx = {
            'from': sender,
            'to': recipient,
            'gas': gas,
            'gasPrice': gas_price,
            'value': value,
            'data': data,
            'nonce': nonce
        }
        return tx

    @staticmethod
    def sign_transaction(tx):
        signed_tx = client.account.signTransaction(tx, private_key)
        return signed_tx

    @staticmethod
    def send_raw_transaction(raw_tx):
        tx_hash = client.sendRawTransaction(raw_tx)
        return tx_hash
