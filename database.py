from sqlite3 import connect, Row
from datetime import datetime
from blockchain import Blockchain
from config import CREDENTIALS, TRANSACTIONS

DATABASE = 'bcio.db'

connection = connect(DATABASE)

# Rows wrapped with the Row class can be accessed both by index (like tuples)
# and case-insensitively by name
connection.row_factory = Row


def setup():
    create_tables()
    seed_credentials()
    seed_transactions()


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
    add_credentials(**CREDENTIALS[Blockchain.ETHEREUM])
    add_credentials(**CREDENTIALS[Blockchain.MULTICHAIN])
    add_credentials(**CREDENTIALS[Blockchain.BITCOIN])


def seed_transactions():
    add_transaction(**TRANSACTIONS[Blockchain.MULTICHAIN])
    add_transaction(**TRANSACTIONS[Blockchain.BITCOIN])


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
