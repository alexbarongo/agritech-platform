import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "..", "data", "farm.db")


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


def get_expenses_with_crops():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT expenses.id, crops.name, expenses.item, expenses.amount
    FROM expenses
    JOIN crops ON expenses.crop_id = crops.id
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def get_total_expenses_per_crop():
    conn = connect()
    cursor = conn.cursor()

    query = """
    SELECT 
        crops.name, 
        COALESCE(SUM(expenses.amount), 0), 
        COUNT(expenses.id)
    FROM crops
    LEFT JOIN expenses ON expenses.crop_id = crops.id
    GROUP BY crops.name
    ORDER BY COALESCE(SUM(expenses.amount), 0) DESC
    """
    cursor.execute(query)
    data = cursor.fetchall()

    conn.close()
    return data


def clear_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses")
    cursor.execute("DELETE FROM crops")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='crops'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='expenses'")

    conn.commit()
    conn.close()
