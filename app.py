import sys
from web3 import Web3, HTTPProvider

gas_limit = 90000
endpoint_url = 'http://localhost:8545'
private_key = '0x4c0883a69102937d6231471b5dbb6204fe5129617082792ae468d01a3f362318'

web3 = Web3(HTTPProvider(endpoint_url))
gas_price = web3.eth.gasPrice
coinbase = web3.eth.coinbase


def sign_transaction(transaction, key):
    return web3.eth.account.signTransaction(transaction, key)


def transaction_count(account):
    return web3.eth.getTransactionCount(account)


def send_raw_transaction(raw_transaction):
    return web3.eth.sendRawTransaction(raw_transaction)


def to_checksum_address(address):
    return web3.toChecksumAddress(address)


def transaction(
    nonce=transaction_count(coinbase),
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
        'data': data,
    }


def main(argv=sys.argv):
    signed_tx = sign_transaction(transaction(), private_key)
    print(signed_tx)
    send_raw_transaction(signed_tx.rawTransaction)  # sender doesn't have enough funds to send tx


if __name__ == '__main__':
    sys.exit(main())
