from web3 import Web3, HTTPProvider
from adapter import Adapter, default_amount, encoding

endpoint_uri = 'http://localhost:8545'

public_key = '0xdeb92221fed1dfe74ea63c00aede6b31f02d6abe'
private_key = \
    'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'

gas_limit = 90000


class EthAdapter(Adapter):
    web3 = Web3(HTTPProvider(endpoint_uri))
    default_address = web3.toChecksumAddress(public_key)

    def retrieve(self, transaction_hash):
        tx = self.get_transaction(transaction_hash)
        return self.to_text(tx.input)

    def get_transaction(self, transaction_hash):
        return self.web3.eth.getTransaction(transaction_hash)

    def to_text(self, data):
        return self.web3.toText(data)

    def store(self, text):
        data = bytes(text, encoding=encoding)
        tx = self.create_transaction(data)
        signed_tx = self.sign_transaction(tx)
        tx_hash = self.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash

    @staticmethod
    def create_transaction(
            data,
            sender=default_address,
            recipient=default_address,
            gas=gas_limit,
            gas_price=web3.eth.gasPrice,
            value=default_amount,
            nonce=web3.eth.getTransactionCount(default_address)):
        return {
            'from': sender,
            'to': recipient,
            'gas': gas,
            'gasPrice': gas_price,
            'value': value,
            'data': data,
            'nonce': nonce
        }

    def sign_transaction(self, transaction):
        return self.web3.eth.account.signTransaction(transaction, private_key)

    def send_raw_transaction(self, raw_transaction):
        return self.web3.eth.sendRawTransaction(raw_transaction)
