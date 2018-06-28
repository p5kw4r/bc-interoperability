import eth_adapter
import mc_adapter


def main():
    original_message = 'Hello, Wörld!'

    transaction_hash = eth_adapter.store(original_message)
    retrieved_message = eth_adapter.retrieve(transaction_hash)
    print(retrieved_message)

    transaction_hash = mc_adapter.store(original_message)
    retrieved_message = mc_adapter.retrieve(transaction_hash)
    print(retrieved_message)


if __name__ == '__main__':
    main()
