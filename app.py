from eth_adapter import EthAdapter


def main():
    eth_adapter = EthAdapter()
    tx_hash = eth_adapter.store('Hello, World!')
    text = eth_adapter.retrieve(tx_hash)
    print(text)


if __name__ == '__main__':
    main()
