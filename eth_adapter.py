from web3 import Web3, HTTPProvider
from config import amount, encoding

endpoint_uri = 'http://localhost:8545'

web3 = Web3(HTTPProvider(endpoint_uri))
client = web3.eth

address = '0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe'
private_key = 'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'


def retrieve(tx_hash):
    tx = get_transaction(tx_hash)
    data = extract_data(tx)
    text = to_text(data)
    return text


def get_transaction(tx_hash):
    tx = client.getTransaction(tx_hash)
    return tx


def extract_data(tx):
    data = tx.input
    return data


def to_text(data):
    text = Web3.toText(data)
    return text


def store(text):
    data = bytes(text, encoding=encoding)
    tx = create_transaction(data)
    signed_tx = sign_transaction(tx)
    tx_hash = send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash


def get_transaction_count():
    tx_count = client.getTransactionCount(address)
    return tx_count


def create_transaction(data):
    tx = {
        'from': address,
        'to': address,
        'gasPrice': client.gasPrice,
        'value': amount,
        'data': data,
        'nonce': get_transaction_count()
    }
    tx['gas'] = estimate_gas(tx)
    return tx


def estimate_gas(tx):
    estimate = client.estimateGas(tx)
    return estimate


def sign_transaction(tx):
    signed_tx = client.account.signTransaction(tx, private_key)
    return signed_tx


def send_raw_transaction(tx):
    tx_hash = client.sendRawTransaction(tx)
    return tx_hash
