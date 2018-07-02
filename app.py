from eth_adapter import EthAdapter
from mc_adapter import MCAdapter
from btc_adapter import BTCAdapter


Adapter = {
    0: EthAdapter,
    1: MCAdapter,
    2: BTCAdapter
}


def store(text, blockchain_id):
    transaction_hash = Adapter[blockchain_id].store(text)
    return transaction_hash


def retrieve(transaction_hash, blockchain_id):
    text = Adapter[blockchain_id].retrieve(transaction_hash)
    return text
