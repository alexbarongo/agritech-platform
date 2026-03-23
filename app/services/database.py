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
        item TEXT NOT NULL, 
        amount REAL NOT NULL,
        crop_id INTEGER,
        FOREIGN KEY (crop_id) REFERENCES crops(id)
    )
    """)

    conn.commit()
    conn.close()


def add_crop(name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO crops (name) VALUES (?)", (name,))

    conn.commit()
    conn.close()


def get_crops():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM crops")
    crops = cursor.fetchall()

    conn.close()
    return crops


def add_expense(item, amount, crop_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (item, amount, crop_id) VALUES (?, ?, ?)",
        (item, amount, crop_id),
    )

    conn.commit()
    conn.close()


def get_expenses():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    conn.close()
    return expenses


def delete_crop(crop_id):
    conn = connect()
    cursor = conn.cursor()

    # delete related expenses first
    cursor.execute("DELETE FROM expenses WHERE crop_id = ?", (crop_id,))

    # then delete crop
    cursor.execute("DELETE FROM crops WHERE id = ?", (crop_id,))

    conn.commit()
    conn.close()


def delete_expenses_by_crop(crop_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE crop_id = ?", (crop_id,))

    conn.commit()
    conn.close()
