from web3 import Web3, HTTPProvider
from config import amount, encoding

endpoint_uri = 'http://localhost:8545'

web3 = Web3(HTTPProvider(endpoint_uri))
client = web3.eth

address = '0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe'
key = 'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'


def retrieve(transaction_hash):
    transaction = get_transaction(transaction_hash)
    data = extract_data(transaction)
    return to_text(data)


def get_transaction(transaction_hash):
    transaction = client.getTransaction(transaction_hash)
    return transaction


def extract_data(transaction):
    return transaction.input


def to_text(data):
    return Web3.toText(data)


def store(text):
    data = bytes(text, encoding=encoding)
    transaction = create_transaction(data)
    signed_transaction = sign_transaction(transaction)
    transaction_hash = send_raw_transaction(signed_transaction.rawTransaction)
    return transaction_hash


def get_transaction_count():
    return client.getTransactionCount(address)


def create_transaction(data):
    transaction = {
        'from': address,
        'to': address,
        'gasPrice': client.gasPrice,
        'value': amount,
        'data': data,
        'nonce': get_transaction_count()
    }
    transaction['gas'] = estimate_gas(transaction)
    return transaction


def estimate_gas(transaction):
    return client.estimateGas(transaction)


def sign_transaction(transaction):
    return client.account.signTransaction(transaction, key)


def send_raw_transaction(transaction):
    transaction_hash = client.sendRawTransaction(transaction)
    return transaction_hash
