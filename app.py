from eth_adapter import EthAdapter
from mc_adapter import MCAdapter


def main():
    message = 'Hello, Wörld!'

    tx_hash = EthAdapter.store(message)
    text = EthAdapter.retrieve(tx_hash)
    print(text)

    tx_hash = MCAdapter.store(message)
    text = MCAdapter.retrieve(tx_hash)
    print(text)


if __name__ == '__main__':
    main()
