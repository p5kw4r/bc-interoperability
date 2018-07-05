from eth_adapter import EthAdapter
from mc_adapter import MCAdapter
from btc_adapter import BTCAdapter
from database import get_blockchain_id
from blockchain import Blockchain


Adapter = {
    Blockchain.ETHEREUM.value: EthAdapter,
    Blockchain.MULTICHAIN.value: MCAdapter,
    Blockchain.BITCOIN.value: BTCAdapter
}


def store(text, blockchain):
    adapter = Adapter[blockchain.value]
    transaction_hash = adapter.store(text)
    return transaction_hash


def retrieve(transaction_hash):
    blockchain_id = get_blockchain_id(transaction_hash)
    adapter = Adapter[blockchain_id]
    text = adapter.retrieve(transaction_hash)
    return text
