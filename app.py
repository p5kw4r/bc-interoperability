from eth_adapter import EthAdapter
from mc_adapter import MCAdapter


def main():
    message = 'Hello, Wörld!'

    eth_adapter = EthAdapter()
    tx_hash = eth_adapter.store(message)
    text = eth_adapter.retrieve(tx_hash)
    print(text)

    mc_adapter = MCAdapter()
    tx_hash = mc_adapter.store(message)
    text = mc_adapter.retrieve(tx_hash)
    print(text)


if __name__ == '__main__':
    main()
