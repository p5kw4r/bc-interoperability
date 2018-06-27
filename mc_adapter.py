from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from adapter import encoding

host = 'localhost'
port = '7324'

# The API credentials for each blockchain are stored in the
# ~/.multichain/[chain-name]/multichain.conf
rpcuser = 'multichainrpc'
rpcpassword = 'GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'

# The private key can be found by running `dumpprivkey [address]` command in
# interactive mode
default_address = '1RuG62c89Vk1V6psGhtAwywan9mWsvFvBv2cLM'
private_key = 'VAUWVB6KStqzemdzXqak77cbkaz6tyYyRbcG3pqBcpP2xNFzAvT8bt2E'


class MCAdapter:
    client = RpcClient(host, port, rpcuser, rpcpassword)

    def retrieve(self, transaction_hash):
        tx = self.get_raw_transaction(transaction_hash)
        data_hex = self.extract_data(tx)
        return self.to_text(data_hex)

    def get_raw_transaction(self, transaction_hash):
        return self.client.getrawtransaction(transaction_hash, verbose=1)

    @staticmethod
    def extract_data(transaction):
        return transaction['vout'][1]['data'][0]

    @staticmethod
    def to_text(data_hex):
        text_bytes = unhexlify(data_hex)
        return text_bytes.decode(encoding=encoding)

    def store(self, text):
        data_hex = self.to_hex(text)
        tx_hex = self.create_raw_send_from(data_hex)
        signed_tx_hex = self.sign_raw_transaction(tx_hex)
        return self.send_raw_transaction(signed_tx_hex)

    @staticmethod
    def to_hex(text):
        text_bytes = bytes(text, encoding=encoding)
        return hexlify(text_bytes)

    def create_raw_send_from(
            self,
            data_hex,
            sender=default_address,
            recipient=default_address,
            amount=0):
        return self.client.createrawsendfrom(
            sender,
            {recipient: amount},
            [data_hex])

    def sign_raw_transaction(self, transaction_hex):
        parent_outputs = []
        signed = self.client.signrawtransaction(
            transaction_hex,
            parent_outputs,
            [private_key])
        if signed['complete']:
            return signed['hex']

    def send_raw_transaction(self, transaction_hash):
        return self.client.sendrawtransaction(transaction_hash)
