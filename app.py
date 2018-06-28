import eth_adapter
import mc_adapter


def main():
    message = 'Hello, Wörld!'

    tx_hash = eth_adapter.store(message)
    text = eth_adapter.retrieve(tx_hash)
    print(text)

    tx_hash = mc_adapter.store(message)
    text = mc_adapter.retrieve(tx_hash)
    print(text)


if __name__ == '__main__':
    main()
