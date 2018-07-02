from eth_adapter import EthAdapter
from mc_adapter import MCAdapter
from btc_adapter import BTCAdapter


def main():
    original_message = 'Hello, Wörld!'

    transaction_hash = EthAdapter.store(original_message)
    retrieved_message = EthAdapter.retrieve(transaction_hash)
    print(retrieved_message)

    transaction_hash = MCAdapter.store(original_message)
    retrieved_message = MCAdapter.retrieve(transaction_hash)
    print(retrieved_message)

    transaction_hash = BTCAdapter.store(original_message)
    retrieved_message = BTCAdapter.retrieve(transaction_hash)
    print(retrieved_message)


if __name__ == '__main__':
    main()
