from web3 import Web3, HTTPProvider

endpoint_url = 'http://localhost:8545'
web3 = Web3(HTTPProvider(endpoint_url))

gas_limit = 90000

public_key = '0xdeb92221fed1dfe74ea63c00aede6b31f02d6abe'
default_address = web3.toChecksumAddress(public_key)
private_key = 'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'


def sign_transaction(transaction, key):
    return web3.eth.account.signTransaction(transaction, key)


def get_transaction_count(account):
    return web3.eth.getTransactionCount(account)


def send_raw_transaction(raw_transaction):
    return web3.eth.sendRawTransaction(raw_transaction)


def get_transaction(transaction_hash):
    return web3.eth.getTransaction(transaction_hash)


def to_checksum_address(address):
    return web3.toChecksumAddress(address)


def create_transaction(
    nonce=get_transaction_count(default_address),
    gas_price=web3.eth.gasPrice,
    gas=gas_limit,
    to=default_address,
    value=0,
    data=b'Hello World!',
    sender=default_address
):
    return {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas,
        'to': to,
        'data': data,
        'value': value,
        'from': sender
    }


def main():
    tx = create_transaction()
    signed_tx = sign_transaction(tx, private_key)
    tx_hash = send_raw_transaction(signed_tx.rawTransaction)
    tx_after = get_transaction(tx_hash)
    print(web3.toText(tx_after.input))


if __name__ == '__main__':
    main()
