from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from adapter import Adapter, default_amount, encoding

host = 'localhost'
port = '7324'

# The API credentials for each blockchain are stored in the
# ~/.multichain/[chain-name]/multichain.conf
rpcuser = 'multichainrpc'
rpcpassword = 'GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'

client = RpcClient(host, port, rpcuser, rpcpassword)

# The private key can be found by running `dumpprivkey [address]` command in
# interactive mode, i.e. `$ multichain-cli [chain-name]`
default_address = '1RuG62c89Vk1V6psGhtAwywan9mWsvFvBv2cLM'
private_key = 'VAUWVB6KStqzemdzXqak77cbkaz6tyYyRbcG3pqBcpP2xNFzAvT8bt2E'


class MCAdapter(Adapter):
    @classmethod
    def retrieve(cls, transaction_hash):
        tx = cls.get_raw_transaction(transaction_hash)
        data_hex = cls.extract_data(tx)
        return cls.to_text(data_hex)

    @staticmethod
    def get_raw_transaction(transaction_hash):
        return client.getrawtransaction(transaction_hash, verbose=1)

    @staticmethod
    def extract_data(transaction):
        # workaround needed because potentially multiple output addresses in
        # single transaction (and also potentially multiple data items)
        return transaction['vout'][1]['data'][0]

    @staticmethod
    def to_text(data_hex):
        text_bytes = unhexlify(data_hex)
        return text_bytes.decode(encoding=encoding)

    @classmethod
    def store(cls, text):
        data_hex = cls.to_hex(text)
        tx_hex = cls.create_raw_send_from(data_hex)
        signed_tx_hex = cls.sign_raw_transaction(tx_hex)
        return cls.send_raw_transaction(signed_tx_hex)

    @staticmethod
    def to_hex(text):
        text_bytes = bytes(text, encoding=encoding)
        return hexlify(text_bytes)

    @staticmethod
    def create_raw_send_from(
            data_hex,
            sender=default_address,
            recipient=default_address,
            amount=default_amount):
        return client.createrawsendfrom(
            sender,
            {recipient: amount},
            [data_hex])

    @staticmethod
    def sign_raw_transaction(transaction_hex):
        parent_outputs = []
        signed = client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [private_key])
        if signed['complete']:
            return signed['hex']

    @staticmethod
    def send_raw_transaction(transaction_hash):
        return client.sendrawtransaction(transaction_hash)
