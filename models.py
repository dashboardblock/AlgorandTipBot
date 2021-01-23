import sqlite3
from sqlite3 import Error


def sql_connection():

    try:
        conn = sqlite3.connect('algorandtipbot.db')
        return conn
    except Error:
        print(Error)

conn = sql_connection()

def create_database(conn):
    conn = sql_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE users(username text PRIMARY KEY, address text, private_key text, passphrase text)")
    c.execute("CREATE TABLE transactions(username_from text, username_to text, amount real)")
    conn.commit()
    c.close


def insert_user(username,address,private_key,passphrase):
    conn = sql_connection()
    c = conn.cursor()
    c.execute('insert into users values (?,?,?,?)',(username,address,private_key,passphrase))
    conn.commit()
    c.close

def insert_transaction(username_from,username_to,amount):
    conn = sql_connection()
    c = conn.cursor()
    c.execute('insert into transactions values (?,?,?)',(username_from,username_to,amount))
    conn.commit()
    c.close

def fetch_user(username):
    conn = sql_connection()
    c = conn.cursor()
    c.execute("SELECT username, address, private_key, passphrase FROM users WHERE username = ?",(username,))
    results = c.fetchall()
    return results