from sqlite3 import connect, Row
from datetime import datetime
from blockchain import Blockchain

DATABASE = 'bcio.db'

connection = connect(DATABASE)

# Rows wrapped with the Row class can be accessed both by index (like tuples)
# and case-insensitively by name
connection.row_factory = Row


def create_tables():
    with connection:
        connection.execute(
            '''
            CREATE TABLE transactions 
            (hash TEXT PRIMARY KEY, 
            blockchain_id INTEGER, 
            issued_at TIMESTAMP)
            '''
        )
        connection.execute(
            '''
            CREATE TABLE credentials 
            (id INTEGER PRIMARY KEY, 
            address TEXT, 
            key TEXT, 
            user TEXT, 
            password TEXT)
            '''
        )


def seed_credentials():
    add_credentials(
        blockchain_id=Blockchain.ETHEREUM.value,
        address='0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe',
        key='d54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'
    )
    add_credentials(
        blockchain_id=Blockchain.MULTICHAIN.value,
        address='1MRQf6mYRDoXjtoKVBi8huxBC69zmSzheYN4yM',
        key='V7BFGjp4wrowNSJDSouXVFJQkwZxMFDScba4SkHYA9aYjEDhLrFBV2Nd',
        user='multichainrpc',
        password='GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'
    )
    add_credentials(
        blockchain_id=Blockchain.BITCOIN.value,
        address='2NGMq7iBuJTeDMQPxSaEQVqMtdt3VQxuN7B',
        key='cS6kdk7zxTCij8HpXHE8Kdnh1uAM46PU5LNtQxpBZ6YjP3t3zgWL',
        user='bitcoinrpc',
        password='f7efda5c189b999524f151318c0c86$d5b51b3beffbc02b724e5d095828e0bc8b2456e9ac8757ae3211a5d9b16a22ae'
    )


def seed_transactions():
    add_transaction(
        transaction_hash='826e7100deeef7def0bfed7f5160ae6ac55a3a0cc8fca660a30488c1755e370d',
        blockchain_id=Blockchain.MULTICHAIN.value
    )
    add_transaction(
        transaction_hash='151d65141a9a4a9c37fc0c8ac7aa23feb0981876b8198a970fb9956ca34e467c',
        blockchain_id=Blockchain.BITCOIN.value
    )


def add_transaction(transaction_hash, blockchain_id):
    now = datetime.now()
    with connection:
        connection.execute(
            'INSERT INTO transactions VALUES (?, ?, ?)',
            (transaction_hash, blockchain_id, now)
        )


def get_latest_transaction(blockchain_id):
    cursor = connection.execute(
        '''
        SELECT hash 
        FROM transactions 
        WHERE blockchain_id=? 
        ORDER BY issued_at DESC 
        LIMIT 1
        ''',
        (blockchain_id,)
    )
    row = cursor.fetchone()
    return row['hash']


def get_blockchain_id(transaction_hash):
    cursor = connection.execute(
        'SELECT blockchain_id FROM transactions WHERE hash=?',
        (transaction_hash,)
    )
    row = cursor.fetchone()
    return row['blockchain_id']


def add_credentials(blockchain_id, address, key, user='', password=''):
    with connection:
        connection.execute(
            '''
            INSERT INTO credentials 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (blockchain_id, address, key, user, password)
        )


def update_credentials(blockchain_id, address, key, user='', password=''):
    with connection:
        connection.execute(
            '''
            UPDATE credentials 
            SET 
            address=?, 
            key=?, 
            user=?, 
            password=? 
            WHERE id=?
            ''',
            (address, key, user, password, blockchain_id)
        )


def get_credentials(blockchain_id):
    cursor = connection.execute(
        'SELECT address, key, user, password FROM credentials WHERE id=?',
        (blockchain_id,)
    )
    row = cursor.fetchone()
    return row
