from binascii import hexlify, unhexlify
from bitcoinrpc.authproxy import AuthServiceProxy
from adapter import Adapter
from config import encoding

# The API credentials are stored in `~/.bitcoin/bitcoin.conf`
rpcuser = 'bitcoinrpc'
rpcpassword = 'f7efda5c189b999524f151318c0c86$d5b51b3beffbc02b724e5d095828e0bc8b2456e9ac8757ae3211a5d9b16a22ae'

endpoint_uri = 'http://%s:%s@127.0.0.1:18332' % (rpcuser, rpcpassword)

address = '2NGMq7iBuJTeDMQPxSaEQVqMtdt3VQxuN7B'
key = 'cS6kdk7zxTCij8HpXHE8Kdnh1uAM46PU5LNtQxpBZ6YjP3t3zgWL'


class BTCAdapter(Adapter):
    client = AuthServiceProxy(endpoint_uri)

    @classmethod
    def get_transaction(cls, transaction_hash):
        transaction_hex = cls.client.getrawtransaction(transaction_hash)
        return cls.client.decoderawtransaction(transaction_hex)

    @classmethod
    def extract_data(cls, transaction):
        output = cls.extract_output(transaction, 1)
        asm = output['scriptPubKey']['asm']
        return asm.split()[1]

    @staticmethod
    def extract_output(transaction, i):
        outputs = transaction['vout']
        return outputs[i]

    @staticmethod
    def to_text(data_hex):
        data = unhexlify(data_hex)
        return data.decode(encoding=encoding)

    @classmethod
    def create_transaction(cls, text, input_transaction_hash=None):
        unspent_output = cls.unspent_output(input_transaction_hash)
        change_amount = cls.change_amount(unspent_output)
        data_hex = cls.to_hex(text)
        transaction_hex = cls.client.createrawtransaction(
            [{'txid': input_transaction_hash, 'vout': 0}],
            {address: change_amount, 'data': data_hex})
        return transaction_hex

    @classmethod
    def unspent_output(cls, transaction_hash):
        transaction = cls.get_transaction(transaction_hash)
        return cls.extract_output(transaction, 0)

    @classmethod
    def change_amount(cls, unspent_output):
        amount = unspent_output['value']
        relay_fee = cls.relay_fee()
        return amount - relay_fee

    @classmethod
    def relay_fee(cls):
        network_info = cls.client.getnetworkinfo()
        return network_info['relayfee']

    @staticmethod
    def to_hex(text):
        data = bytes(text, encoding=encoding)
        data_hex = hexlify(data)
        return data_hex.decode(encoding=encoding)

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
