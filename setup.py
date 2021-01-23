import os
import models

BOT_NAME = os.getenv('BOT_NAME', 'Token Not found')
BOT_ADDRESS = os.getenv('BOT_ADDRESS', 'Token Not found')
BOT_PRIVATE_KEY = os.getenv('BOT_PRIVATE_KEY', 'Token Not found')
BOT_MNEMONIC = os.getenv('BOT_MNEMONIC', 'Token Not found')

conn = models.sql_connection()
models.create_database(conn)
models.insert_user(BOT_NAME,BOT_ADDRESS,BOT_PRIVATE_KEY,BOT_MNEMONIC)