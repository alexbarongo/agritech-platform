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
        name TEXT NOT NULL,
        planting_date TEXT,
        field_size REAL,
        planted_quantity INTEGER,
        harvest_date TEXT,
        harvest_quantity REAL,
        selling_price REAL
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


def add_crop(
    name,
    planting_date=None,
    field_size=None,
    planted_quantity=None,
    harvest_date=None,
    harvest_quantity=None,
    selling_price=None,
):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO crops (
            name, planting_date,field_size, planted_quantity,
            harvest_date, harvest_quantity, selling_price
    ) VALUES (?,?,?,?,?,?,?)
    """,
        (
            name,
            planting_date,
            field_size,
            planted_quantity,
            harvest_date,
            harvest_quantity,
            selling_price,
        ),
    )

    conn.commit()
    conn.close()


def get_crops():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, name, planting_date, field_size,
           planted_quantity, harvest_date,
           harvest_quantity,selling_price
    FROM crops
    """)
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


def migrate_crops_table():
    conn = connect()
    cursor = conn.cursor()

    new_columns = [
        ("planting_date", "TEXT"),
        ("field_size", "REAL"),
        ("planted_quantity", "INTEGER"),
        ("harvest_date", "TEXT"),
        ("harvest_quantity", "REAL"),
        ("selling_price", "REAL"),
    ]

    for column_name, column_type in new_columns:
        try:
            cursor.execute(f"ALTER TABLE crops ADD COLUMN {column_name} {column_type}")

        except Exception as e:
            print(f"Column {column_name} skipped: {e}")

    conn.commit()
    conn.close()


def get_profit_report():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            crops.id,
            crops.name,
            crops.harvest_quantity,
            crops.selling_price,
            COALESCE(SUM(expenses.amount), 0) as total_expenses,
            COALESCE(crops.harvest_quantity * crops.selling_price, 0) as revenue,
            COALESCE(crops.harvest_quantity * crops.selling_price, 0) -
            COALESCE(SUM(expenses.amount), 0) as profit
        FROM crops
        LEFT JOIN expenses ON expenses.crop_id = crops.id
        GROUP BY crops.id
        ORDER BY profit DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data


def record_harvest(crop_id, harvest_quantity, harvest_date, selling_price):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE crops
        SET harvest_quantity = ?,
            harvest_date = ?,
            selling_price = ?
        WHERE id = ?
    """,
        (harvest_quantity, harvest_date, selling_price, crop_id),
    )

    conn.commit()
    conn.close()
