from eth_adapter import EthAdapter
from mc_adapter import MCAdapter
from btc_adapter import BTCAdapter


Adapter = {
    0: EthAdapter,
    1: MCAdapter,
    2: BTCAdapter
}


def store(text, blockchain_id, input_transaction_hash=None):
    adapter = Adapter[blockchain_id]
    transaction_hash = adapter.store(text, input_transaction_hash)
    return transaction_hash


def retrieve(transaction_hash, blockchain_id):
    adapter = Adapter[blockchain_id]
    text = adapter.retrieve(transaction_hash)
    return text
