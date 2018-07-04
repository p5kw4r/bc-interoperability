from sqlite3 import connect, Row
from datetime import datetime

database = 'bcio.db'

connection = connect(database)
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
            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
            address TEXT, 
            key TEXT, 
            user TEXT, 
            password TEXT)
            '''
        )


def seed_credentials():
    add_credentials(
        '0xDEB92221FED1Dfe74eA63c00AEde6b31F02d6ABe',
        'd54db06062615cf2fb8133b96aa8c2becf7524c7ea7bf7f0387ee9b903b6b662'
    )
    add_credentials(
        '18DcW1noCMnpmFwo9qe7aSCe6L7hMjhmhyWjBf',
        'VEuzxDqs2KpvWhYB8uRvW3dNzEng16P496V66Zb7tnnY46LKAoqxNAv8',
        'multichainrpc',
        'GkHfnch8QBgqvZJeMLyb57h42h6TZREr25Uhp5iZ8T2E'
    )
    add_credentials(
        '2NGMq7iBuJTeDMQPxSaEQVqMtdt3VQxuN7B',
        'cS6kdk7zxTCij8HpXHE8Kdnh1uAM46PU5LNtQxpBZ6YjP3t3zgWL',
        'bitcoinrpc',
        'f7efda5c189b999524f151318c0c86$d5b51b3beffbc02b724e5d095828e0bc8b2456e9ac8757ae3211a5d9b16a22ae'
    )


def seed_transactions():
    add_transaction(
        '4bcc37b5750a5b23e495259d47971176fcee0022d5e9769d2d90d4af7eec9f86',
        2
    )
    add_transaction(
        '1f952dadf43a25fde46a9799181d0cdde18920dad227d75f340cb90d0a1ecbdf',
        3
    )


def add_transaction(transaction_hash, blockchain_id):
    now = datetime.now()
    with connection:
        connection.execute(
            'INSERT INTO transactions VALUES (?, ?, ?)',
            (transaction_hash, blockchain_id, now)
        )


def get_latest_transaction_hash(blockchain_id):
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


def add_credentials(address, key, user='', password=''):
    with connection:
        connection.execute(
            '''
            INSERT INTO credentials 
            (address, 
            key, 
            user, 
            password) 
            VALUES (?, ?, ?, ?)
            ''',
            (address, key, user, password)
        )


def update_credentials(blockchain_id, address, key, user='', password=''):
    with connection:
        connection.execute(
            '''
            UPDATE credentials SET 
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
