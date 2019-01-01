import os
from blockchain import Blockchain, blockchain
from credential import credential
from transaction import transaction

AMOUNT = 0
ENCODING = 'utf-8'
DATABASE = 'bcio.db'
BLOCKCHAINS = (
    blockchain(
        blockchain=Blockchain.ETHEREUM,
        name='ETHEREUM'
    ),
    blockchain(
        blockchain=Blockchain.MULTICHAIN,
        name='MULTICHAIN'
    ),
    blockchain(
        blockchain=Blockchain.BITCOIN,
        name='BITCOIN'
    )
)
CREDENTIALS = (
    credential(
        blockchain=Blockchain.ETHEREUM,
        address=os.environ['ETH_ADDR'],
        key=os.environ['ETH_KEY']
    ),
    credential(
        blockchain=Blockchain.MULTICHAIN,
        address=os.environ['MC_ADDR'],
        key=os.environ['MC_KEY'],
        user=os.environ['MC_USER'],
        password=os.environ['MC_PASS']
    ),
    credential(
        blockchain=Blockchain.BITCOIN,
        address=os.environ['BTC_ADDR'],
        key=os.environ['BTC_KEY'],
        user=os.environ['BTC_USER'],
        password=os.environ['BTC_PASS']
    )
)
TRANSACTIONS = (
    transaction(
        transaction_hash=os.environ['MC_TX'],
        blockchain=Blockchain.MULTICHAIN
    ),
    transaction(
        transaction_hash=os.environ['BTC_TX'],
        blockchain=Blockchain.BITCOIN
    )
)
