import sqlite3

DB_NAME = "data/farm.db"


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS crops ( 
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name TEXT NOT NULL
        )
    """)

    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        item TEXT NOT NULL, amount REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()
