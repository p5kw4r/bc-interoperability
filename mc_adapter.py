from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from adapter import Adapter
from config import AMOUNT, ENCODING
from database import \
    get_credentials, \
    add_transaction, \
    get_latest_transaction_hash

BLOCKCHAIN_ID = 2
HOST = 'localhost'
PORT = '7324'


class MCAdapter(Adapter):

    credentials = get_credentials(BLOCKCHAIN_ID)
    address = credentials['address']
    key = credentials['key']
    rpcuser = credentials['user']
    rpcpassword = credentials['password']
    client = RpcClient(HOST, PORT, rpcuser, rpcpassword)

    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getrawtransaction(transaction_hash, verbose=1)

    @classmethod
    def extract_data(cls, transaction):
        # workaround needed because potentially multiple output addresses in
        # single transaction (and also potentially multiple data items)
        output = cls.extract_output(transaction, 1)
        return output['data'][0]

    @staticmethod
    def extract_output(transaction, output_index):
        outputs = transaction['vout']
        return outputs[output_index]

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        return data.decode(ENCODING)

    @classmethod
    def create_transaction(cls, text):
        input_transaction_hash = get_latest_transaction_hash(BLOCKCHAIN_ID)
        data_hex = cls.to_hex(text)
        inputs = [{'txid': input_transaction_hash, 'vout': 0}]
        output = {cls.address: AMOUNT}
        transaction_hex = cls.client.createrawtransaction(
            inputs,
            output,
            [data_hex]
        )
        return transaction_hex

    @staticmethod
    def to_hex(text):
        data = bytes(text, ENCODING)
        return hexlify(data)

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
        add_transaction(transaction_hash, BLOCKCHAIN_ID)
