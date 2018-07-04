from binascii import hexlify, unhexlify
from bitcoinrpc.authproxy import AuthServiceProxy
from adapter import Adapter
from config import ENCODING
import database

BLOCKCHAIN_ID = 3


class BTCAdapter(Adapter):
    credentials = database.get_credentials(BLOCKCHAIN_ID)
    address = credentials['address']
    key = credentials['key']
    rpcuser = credentials['user']
    rpcpassword = credentials['password']
    endpoint_uri = 'http://%s:%s@127.0.0.1:18332' % (rpcuser, rpcpassword)
    client = AuthServiceProxy(endpoint_uri)

    @classmethod
    def get_transaction(cls, transaction_hash):
        transaction_hex = cls.client.getrawtransaction(transaction_hash)
        return cls.client.decoderawtransaction(transaction_hex)

    @classmethod
    def extract_data(cls, transaction):
        output = cls.extract_output(transaction, 1)
        asm = output['scriptPubKey']['asm']
        _, data = asm.split()
        return data

    @staticmethod
    def extract_output(transaction, output_index):
        outputs = transaction['vout']
        return outputs[output_index]

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        return data.decode(encoding=ENCODING)

    @classmethod
    def create_transaction(cls, text):
        input_transaction_hash = database.get_latest_transaction_hash(
            BLOCKCHAIN_ID
        )
        change = cls.get_change(input_transaction_hash)
        data_hex = cls.to_hex(text)
        inputs = [{'txid': input_transaction_hash, 'vout': 0}]
        output = {cls.address: change, 'data': data_hex}
        transaction_hex = cls.client.createrawtransaction(inputs, output)
        return transaction_hex

    @classmethod
    def get_change(cls, transaction_hash):
        amount = cls.extract_amount(transaction_hash)
        relay_fee = cls.get_relay_fee()
        return amount - relay_fee

    @classmethod
    def extract_amount(cls, transaction_hash):
        transaction = cls.get_transaction(transaction_hash)
        output = cls.extract_output(transaction, 0)
        return output['value']

    @classmethod
    def get_relay_fee(cls):
        network_info = cls.client.getnetworkinfo()
        return network_info['relayfee']

    @staticmethod
    def to_hex(text):
        data = bytes(text, encoding=ENCODING)
        data_hex = hexlify(data)
        return data_hex.decode(encoding=ENCODING)

    @classmethod
    def sign_transaction(cls, transaction_hex):
        parent_outputs = []
        signed_transaction = cls.client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [cls.key]
        )
        assert signed_transaction['complete']
        return signed_transaction['hex']

    @classmethod
    def send_raw_transaction(cls, transaction_hex):
        transaction_hash = cls.client.sendrawtransaction(transaction_hex)
        return transaction_hash

    @staticmethod
    def add_transaction_to_database(transaction_hash):
        database.add_transaction(transaction_hash, BLOCKCHAIN_ID)
