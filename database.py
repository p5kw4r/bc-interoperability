from sqlite3 import connect, Row
from datetime import datetime
from blockchain import Blockchain
from config import DATABASE, CREDENTIALS, TRANSACTIONS

connection = connect(DATABASE)
# Rows wrapped with the Row class can be accessed both by index (like tuples)
# and case-insensitively by name
connection.row_factory = Row


def setup():
    drop_tables_if_exist()
    create_tables()
    seed_credentials()
    seed_transactions()


def drop_tables_if_exist():
    with connection:
        connection.execute('DROP TABLE IF EXISTS credentials')
        connection.execute('DROP TABLE IF EXISTS transactions')


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
    for credentials in CREDENTIALS:
        add_credentials(**credentials)


def seed_transactions():
    for transaction in TRANSACTIONS:
        add_transaction(**transaction)


def add_transaction(transaction_hash, blockchain):
    blockchain_id = blockchain.value
    now = datetime.now()
    with connection:
        connection.execute(
            'INSERT INTO transactions VALUES (?, ?, ?)',
            (transaction_hash, blockchain_id, now)
        )


def get_latest_transaction(blockchain):
    blockchain_id = blockchain.value
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


def get_blockchain(transaction_hash):
    cursor = connection.execute(
        'SELECT blockchain_id FROM transactions WHERE hash=?',
        (transaction_hash,)
    )
    row = cursor.fetchone()
    blockchain_id = row['blockchain_id']
    return Blockchain(blockchain_id)


def add_credentials(blockchain, address, key, user='', password=''):
    blockchain_id = blockchain.value
    with connection:
        connection.execute(
            '''
            INSERT INTO credentials 
            VALUES (?, ?, ?, ?, ?)
            ''',
            (blockchain_id, address, key, user, password)
        )


def update_credentials(blockchain, address, key, user='', password=''):
    blockchain_id = blockchain.value
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


def get_credentials(blockchain):
    blockchain_id = blockchain.value
    cursor = connection.execute(
        'SELECT address, key, user, password FROM credentials WHERE id=?',
        (blockchain_id,)
    )
    row = cursor.fetchone()
    return row
