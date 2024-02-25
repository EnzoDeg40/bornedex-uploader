import sqlite3
import os

conn = sqlite3.connect('sqlite.db', check_same_thread=False) # TODO: remove check_same_thread
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bornes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT DEFAULT CURRENT_TIMESTAMP,
        name TEXT,
        x TEXT,
        y TEXT,
        alt TEXT,
        city TEXT,
        wiki TEXT,
        description TEXT,
        discord_userid TEXT,
        discord_username TEXT,
        discord_email TEXT,
        discord_avatar TEXT,
        is_valid BOOLEAN DEFAULT 0
    )
''')

conn.commit()
conn.close()

if not os.path.exists("uploads"):
    os.makedirs("uploads")
