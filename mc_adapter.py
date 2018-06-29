from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from adapter import Adapter
from config import amount, encoding

host = 'localhost'
port = '7324'

# The API credentials for each blockchain are stored in the
# ~/.multichain/[chain-name]/multichain.conf
rpcuser = 'multichainrpc'
rpcpassword = 'GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'

# The private key can be found by running `dumpprivkey [address]` command in
# interactive mode, i.e. `$ multichain-cli [chain-name]`
address = '1RuG62c89Vk1V6psGhtAwywan9mWsvFvBv2cLM'
key = 'VAUWVB6KStqzemdzXqak77cbkaz6tyYyRbcG3pqBcpP2xNFzAvT8bt2E'


class MCAdapter(Adapter):
    client = RpcClient(host, port, rpcuser, rpcpassword)

    @classmethod
    def get_transaction(cls, transaction_hash):
        return cls.client.getrawtransaction(transaction_hash, verbose=1)

    @staticmethod
    def extract_data(transaction):
        # workaround needed because potentially multiple output addresses in
        # single transaction (and also potentially multiple data items)
        output = transaction['vout'][1]
        return output['data'][0]

    @staticmethod
    def to_text(data_hex):
        text_bytes = unhexlify(data_hex)
        return text_bytes.decode(encoding=encoding)

    @staticmethod
    def to_hex(text):
        data = bytes(text, encoding=encoding)
        return hexlify(data)

    @classmethod
    def create_transaction(cls, text):
        data_hex = cls.to_hex(text)
        transaction_hex = cls.client.createrawsendfrom(
            address,
            {address: amount},
            [data_hex])
        return transaction_hex

    @classmethod
    def sign_transaction(cls, transaction_hex):
        parent_outputs = []
        signed_transaction = cls.client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [key])
        assert signed_transaction['complete']
        return signed_transaction['hex']

    @classmethod
    def send_raw_transaction(cls, transaction_hex):
        transaction_hash = cls.client.sendrawtransaction(transaction_hex)
        return transaction_hash
