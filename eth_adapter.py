from web3 import Web3, HTTPProvider

endpoint_url = 'http://localhost:8545'
web3 = Web3(HTTPProvider(endpoint_url))

gas_price = web3.eth.gasPrice
gas_limit = 90000
encoding = 'utf-8'
public_key = '0xdeb92221fed1dfe74ea63c00aede6b31f02d6abe'
private_key = 'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'
default_address = web3.toChecksumAddress(public_key)


def to_checksum_address(address):
    return web3.toChecksumAddress(address)


def store(text, key):
    tx = create_transaction(text)
    signed_tx = sign_transaction(tx, key)
    tx_hash = send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash


def get_transaction_count(account):
    return web3.eth.getTransactionCount(account)


def create_transaction(
        text,
        sender=default_address,
        recipient=default_address,
        gas=gas_limit,
        gas_price=gas_price,
        value=0,
        nonce=get_transaction_count(default_address)):
    return {
        'from': sender,
        'to': recipient,
        'gas': gas,
        'gasPrice': gas_price,
        'value': value,
        'data': bytes(text, encoding=encoding),
        'nonce': nonce
    }


def sign_transaction(transaction, key):
    return web3.eth.account.signTransaction(transaction, key)


def send_raw_transaction(raw_transaction):
    return web3.eth.sendRawTransaction(raw_transaction)


def retrieve(transaction_hash):
    tx = get_transaction(transaction_hash)
    return extract_text(tx)


def extract_text(transaction):
    return web3.toText(transaction.input)


def get_transaction(transaction_hash):
    return web3.eth.getTransaction(transaction_hash)
