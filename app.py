from eth_adapter import store, retrieve


def main():
    tx_hash = store('Hello, World!')
    text = retrieve(tx_hash)
    print(text)


if __name__ == '__main__':
    main()
