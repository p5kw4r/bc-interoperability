# bcio

A project towards blockchain interoperability.

## Dependencies

This project is built with:

- [Sqlite3](https://www.sqlite.org/index.html) as dbms
- [Web3.py](https://web3py.readthedocs.io/en/stable/) for Ethereum integration
- [mcrpc](https://github.com/coblo/mcrpc) for MultiChain integration
- [python-bitcoinrpc](https://github.com/jgarzik/python-bitcoinrpc) for Bitcoin integration

## Setup

### Python

Install packages using your favourite package manager:

```
# pacman -S python python-pip
```

#### With virtual environment

Create a virtual environment within the project (for `python >= 3.3`):

```
$ python -m venv venv
```

Activate virtual environment:

```
$ source venv/bin/activate
```

Install dependencies:

```
(venv) $ pip install web3 mcrpc python-bitcoinrpc
```

Deactivate virtual environment:

```
(venv) $ deactivate
```

#### Without virtual environment

Install dependencies:

```
$ pip install --user web3 mcrpc python-bitcoinrpc
```

### Database

Install package using your favourite package manager:

```
# pacman -S sqlite
```

Run the database setup:

```python
from bcio import database

database.setup()
```

> Calling the `setup` function of the [`database`](database.py) module will:
>
> 1. drop `credentials` and `transactions` tables if they already exist
> 2. create tables for storing `credentials` and `transactions`
> 3. seed the `credentials` table with credentials for Ethereum, MultiChain and Bitcoin
> 4. seed the `transactions` table with input transactions for MultiChain and Bitcoin

> Seed values are read from the [`config`](config.py) module.

### Ethereum

Install package using your favourite package manager:

```
# pacman -S go-ethereum
```

Create the genesis block. For a private network, you usually want a custom genesis block. Here's an example of a custom `genesis.json` file:

```
{
    "config": {
        "chainId": 15,
        "homesteadBlock": 0,
        "eip155Block": 0,
        "eip158Block": 0
    },
    "difficulty": "200000000",
    "gasLimit": "2100000"
}
```

To create a database that uses this genesis block, run the following command. This will import and set the canonical genesis block for your chain:

```
$ geth --datadir path/to/custom/data/folder init genesis.json
```

> Future runs of `geth` on this data directory will use the genesis block you have defined.

Launch the `geth` client and allow rpc connections:

```
$ geth --datadir path/to/custom/data/folder --networkid 3107 --fast --rpc --rpcapi eth,web3,personal,net,miner,admin
```

Enter interactive mode:

```
$ geth attach http://127.0.0.1:8545
```

In interactive mode, set the account that will receive ether from the mining process:

```
> miner.setEtherbase(eth.accounts[0])

true
```

Launch the mining process with 2 threads:

```
> miner.start(2)

null
```

> You must mine every transaction in your private network. Thus, it makes sense to always leave the miner running.

To stop the mining process:

```
$ miner.stop()

true
```

### MultiChain

On Arch Linux, a package is available from the Arch User Repository:

```
$ yay -S multichain-alpha
```

First we will create a new blockchain named `chain1`:

```
$ multichain-util create chain1
```

> The API credentials for the blockchain are stored in the `~/.multichain/chain1/multichain.conf` file.
> The blockchain's settings are stored in the `~/.multichain/chain1/params.dat` file.

> Once the blockchain is initialized, **these parameters cannot be changed**.

Initialize the blockchain, including creating the genesis block:

```
$ multichaind chain1 -daemon
```

Enter interactive mode:

```
$ multichain-cli chain1
```

In interactive mode, generate public/private key pairs that are not stored in the wallet or drawn from the node's key pool (for external key management):

```
> createkeypairs

[
    {
        "address" : "1LKfR5yQVKx3YJ27enyKDNske7XFHzkN6bm43Y",
        "pubkey" : "0323187cd83c9dde13f223b5df1fb2899e645e8b0cd1fa73ae61c41b07ce9cd7a6",
        "privkey" : "VHrFLuvdBeb1oVTmKD48Sdm1ovoc8mS5pbrk2gpKhCUWh72LavvAF8jx"
    }
]
```

Before, we can use the generated address in transactions, we have to grant it permission to send and receive within the blockchain:

```
> grant 1LKfR5yQVKx3YJ27enyKDNske7XFHzkN6bm43Y send,receive

ddcca7c4d57bb185443914cdac7a6a9d3b93743d8f39cd61a989b8bdfd09e49b
```

> This command will return a transaction hash (which can be used as seed transaction).

Stop the blockchain:

```
> stop
```

### Bitcoin

Install packages using your favourite package manager:

```
# pacman -S bitcoind bitcoin-cli
```

> A GUI client is available in `bitcoin-qt`.

To connect to the public testnet of Bitcoin (`testnet3`), the following settings are required in the `~/.bitcoin/bitcoin.conf` file:

```
testnet = 1
rpcuser = 'bitcoinrpc'
rpcpassword = 'password'
```

> A more complete sample configuration file is available [here](https://github.com/bitcoin/bitcoin/blob/master/contrib/debian/examples/bitcoin.conf).

> In `bitcoind` rpc connections are allowed by default, in `bitcoin-qt` `server = 1` is required in the configuration file to allow rpc connections.

To sync the node with the public testnet:

```
$ bitcoind
```

The progress of the syncing process can be monitored with:

```
$ tail -f ~/.bitcoin/testnet3/debug.log
```

To stop the blockchain:

```
$ bitcoin-cli stop
```

## Usage

Store a text message on the Ethereum blockchain and retrieve it using the transaction hash:

```python
from bcio import store, retrieve, Blockchain

tx_hash = store('Hello World!', Blockchain.ETHEREUM)
text = retrieve(tx_hash)
```

> Alternatively, the module comes with integration for MultiChain (`Blockchain.MULTICHAIN`) and Bitcoin (`Blockchain.BITCOIN`).
