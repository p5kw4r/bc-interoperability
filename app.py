from eth_adapter import store, retrieve, private_key


def main():
    tx_hash = store('Hello, World!', private_key)
    text = retrieve(tx_hash)
    print(text)


if __name__ == '__main__':
    main()
