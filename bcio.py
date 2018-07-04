from eth_adapter import EthAdapter
from mc_adapter import MCAdapter
from btc_adapter import BTCAdapter
import database


Adapter = {
    1: EthAdapter,
    2: MCAdapter,
    3: BTCAdapter
}


def store(text, blockchain_id):
    adapter = Adapter[blockchain_id]
    transaction_hash = adapter.store(text)
    return transaction_hash


def retrieve(transaction_hash):
    blockchain_id = database.get_blockchain_id(transaction_hash)
    adapter = Adapter[blockchain_id]
    text = adapter.retrieve(transaction_hash)
    return text
