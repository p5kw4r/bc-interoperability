from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from config import amount, encoding

host = 'localhost'
port = '7324'

# The API credentials for each blockchain are stored in the
# ~/.multichain/[chain-name]/multichain.conf
rpcuser = 'multichainrpc'
rpcpassword = 'GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'

client = RpcClient(host, port, rpcuser, rpcpassword)

# The private key can be found by running `dumpprivkey [address]` command in
# interactive mode, i.e. `$ multichain-cli [chain-name]`
address = '1RuG62c89Vk1V6psGhtAwywan9mWsvFvBv2cLM'
private_key = 'VAUWVB6KStqzemdzXqak77cbkaz6tyYyRbcG3pqBcpP2xNFzAvT8bt2E'


def retrieve(transaction_hash):
    transaction = get_transaction(transaction_hash)
    data_hex = extract_data(transaction)
    return to_text(data_hex)


def get_transaction(transaction_hash):
    return client.getrawtransaction(transaction_hash, verbose=1)


def extract_data(transaction):
    # workaround needed because potentially multiple output addresses in
    # single transaction (and also potentially multiple data items)
    output = transaction['vout'][1]
    return output['data'][0]


def to_text(data_hex):
    text_bytes = unhexlify(data_hex)
    return text_bytes.decode(encoding=encoding)


def store(text):
    data_hex = to_hex(text)
    transaction_hex = create_transaction(data_hex)
    signed_transaction_hex = sign_transaction(transaction_hex)
    transaction_hash = send_raw_transaction(signed_transaction_hex)
    return transaction_hash


def to_hex(text):
    data = bytes(text, encoding=encoding)
    return hexlify(data)


def create_transaction(data_hex):
    transaction_hex = client.createrawsendfrom(
        address,
        {address: amount},
        [data_hex])
    return transaction_hex


def sign_transaction(transaction_hex):
    parent_outputs = []
    signed_transaction = client.signrawtransaction(
        transaction_hex,
        parent_outputs,
        [private_key])
    if signed_transaction['complete']:
        signed_transaction_hex = signed_transaction['hex']
        return signed_transaction_hex


def send_raw_transaction(transaction_hex):
    transaction_hash = client.sendrawtransaction(transaction_hex)
    return transaction_hash
