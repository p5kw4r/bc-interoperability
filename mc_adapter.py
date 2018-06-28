from binascii import hexlify, unhexlify
from mcrpc import RpcClient
from config import default_amount, encoding

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


def retrieve(tx_hash):
    tx = get_transaction(tx_hash)
    data_hex = extract_data(tx)
    text = to_text(data_hex)
    return text


def get_transaction(tx_hash):
    tx = client.getrawtransaction(tx_hash, verbose=1)
    return tx


def extract_data(tx):
    # workaround needed because potentially multiple output addresses in
    # single transaction (and also potentially multiple data items)
    output = tx['vout'][1]
    data = output['data'][0]
    return data


def to_text(data_hex):
    text_bytes = unhexlify(data_hex)
    text = text_bytes.decode(encoding=encoding)
    return text


def store(text):
    data_hex = to_hex(text)
    tx_hex = create_transaction(data_hex)
    signed_tx_hex = sign_transaction(tx_hex)
    tx_hash = send_raw_transaction(signed_tx_hex)
    return tx_hash


def to_hex(text):
    data = bytes(text, encoding=encoding)
    data_hex = hexlify(data)
    return data_hex


def create_transaction(
        data_hex,
        sender=default_address,
        recipient=default_address,
        amount=default_amount):
    tx_hex = client.createrawsendfrom(sender, {recipient: amount}, [data_hex])
    return tx_hex


def sign_transaction(tx_hex):
    parent_outputs = []
    signed_tx = client.signrawtransaction(tx_hex, parent_outputs, [private_key])
    if signed_tx['complete']:
        signed_tx_hex = signed_tx['hex']
        return signed_tx_hex


def send_raw_transaction(tx_hex):
    tx_hash = client.sendrawtransaction(tx_hex)
    return tx_hash
