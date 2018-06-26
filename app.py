import sys
from web3 import Web3, HTTPProvider

endpoint_url = 'http://localhost:8545'
web3 = Web3(HTTPProvider(endpoint_url))

private_key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'
gas_limit = 90000
gas_price = web3.eth.gasPrice
coinbase = web3.eth.coinbase  # web3.eth.accounts[0]
default_account = web3.eth.accounts[0]


def sign_transaction(transaction, key):
    return web3.eth.account.signTransaction(transaction, key)


def transaction_count(account):
    return web3.eth.getTransactionCount(account)


def send_raw_transaction(raw_transaction):
    return web3.eth.sendRawTransaction(raw_transaction)


def send_transaction(transaction):
    return web3.eth.sendTransaction(transaction)


def get_transaction(tx_hash):
    return web3.eth.getTransaction(tx_hash)


def to_checksum_address(address):
    return web3.toChecksumAddress(address)


def transaction(
        nonce=transaction_count(default_account),
        gas_price=gas_price,
        gas=gas_limit,
        to=to_checksum_address('0xd3cda913deb6f67967b99d67acdfa1712c293601'),
        data=b''
):
    return {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas,
        'to': to,
        'data': data
    }


def transaction_with_sender(
    nonce=transaction_count(default_account),
    gas_price=gas_price,
    gas=gas_limit,
    to=to_checksum_address('0xd3cda913deb6f67967b99d67acdfa1712c293601'),
    data=b'',
    sender=default_account
):
    return {
        'nonce': nonce,
        'gasPrice': gas_price,
        'gas': gas,
        'to': to,
        'data': data,
        'from': sender
    }


def main(argv=sys.argv):
    tx = transaction()
    signed_tx = sign_transaction(tx, private_key)
    print(signed_tx, '\n')
    # tx_hash = send_raw_transaction(signed_tx.rawTransaction)  # sender doesn't have enough funds to send tx
    # print(tx_hash, '\n')

    tx_before = transaction_with_sender()
    tx_hash = send_transaction(tx_before)
    tx_after = get_transaction(tx_hash)
    print(tx_before, '\n')
    print(tx_after)  # does not have a data field anymore


if __name__ == '__main__':
    sys.exit(main())
