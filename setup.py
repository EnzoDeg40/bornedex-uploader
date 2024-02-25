import sqlite3
import os

conn = sqlite3.connect('sqlite.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        password TEXT,
        discord_id TEXT NOT NULL UNIQUE,
        discord_username TEXT
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bornes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT
        x REAL NOT NULL,
        y REAL NOT NULL,
        alt INTEGER,
        city TEXT,
        wiki TEXT,
        user_id INTEGER,
        is_valid BOOLEAN DEFAULT 0
    );
''')

conn.commit()
conn.close()

if not os.path.exists("uploads"):
    os.makedirs("uploads")
