import os
import sqlite3
from fileinput import close

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.environ.get("DATA_DIR", os.path.join(BASE_DIR, "..", "data"))
DB_NAME = os.path.join(DATA_DIR, "farm.db")
os.makedirs(DATA_DIR, exist_ok=True)


def connect():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crops (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        planting_date TEXT,
        field_size REAL,
        planted_quantity INTEGER,
        harvest_date TEXT,
        harvest_quantity REAL,
        selling_price REAL,
        FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item TEXT NOT NULL,
        amount REAL NOT NULL,
        crop_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (crop_id) REFERENCES crops(id)
    )
    """)

    conn.commit()
    conn.close()


def create_user(name, email, hashed_password):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
                INSERT INTO users (name, email, password)
                VALUES (?, ?, ?)
            """,
            (name, email, hashed_password),
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Error creating user: {e}")
        return False
    finally:
        conn.close()


def get_user_by_email(email):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, password FROM users WHERE email = ?", (email,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def add_crop(
    user_id,
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
            user_id, name, planting_date,field_size, planted_quantity,
            harvest_date, harvest_quantity, selling_price
    ) VALUES (?,?,?,?,?,?,?, ?)
    """,
        (
            user_id,
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


def get_crops_by_user(user_id: int):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT id, name, planting_date, field_size,
           planted_quantity, harvest_date,
           harvest_quantity,selling_price
    FROM crops
    WHERE user_id = ?
    """,
        (user_id,),
    )

    crops = cursor.fetchall()
    conn.close()
    return crops


def add_expense(user_id, item, amount, crop_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses (user_id, item, amount, crop_id) VALUES (?, ?, ?, ?)",
        (user_id, item, amount, crop_id),
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


def get_expenses_by_user(user_id: int):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
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


def delete_expense(expense_id: int):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))

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


def get_expenses_with_crops_by_user(user_id: int):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
    SELECT
        expenses.id,
        COALESCE(crops.name, 'No Crop'),
        expenses.item,
        expenses.amount
    FROM expenses
    LEFT JOIN crops ON expenses.crop_id = crops.id
    WHERE crops.user_id = ?
    """,
        (user_id,),
    )

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


def get_total_expenses_per_crop_by_user(user_id: int):
    conn = connect()
    cursor = conn.cursor()

    query = """
    SELECT
        crops.name,
        COALESCE(SUM(expenses.amount), 0),
        COUNT(expenses.id)
    FROM crops
    LEFT JOIN expenses ON expenses.crop_id = crops.id
    WHERE crops.user_id = ?
    GROUP BY crops.name
    ORDER BY COALESCE(SUM(expenses.amount), 0) DESC
    """
    cursor.execute(query, (user_id,))
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
        ("user_id", "INTEGER"),
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


def migrate_expenses_table():
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("ALTER TABLE expenses ADD COLUMN user_id INTEGER")
        print("✅ user_id column added to expenses")
    except Exception as e:
        print(f"⚠️ Migration skipped (likely already exists): {e}")

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


def get_profit_report_by_user(user_id: int):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            crops.id,
            crops.name,
            COALESCE(crops.harvest_quantity, 0),
            COALESCE(crops.selling_price, 0),
            COALESCE(SUM(expenses.amount), 0) as total_expenses,
            COALESCE(crops.harvest_quantity, 0) * COALESCE(crops.selling_price, 0) as revenue,
            (COALESCE(crops.harvest_quantity, 0) * COALESCE(crops.selling_price, 0)) -
            COALESCE(SUM(expenses.amount), 0) as profit
        FROM crops
        LEFT JOIN expenses ON expenses.crop_id = crops.id
        WHERE crops.user_id = ?
        GROUP BY crops.id
        ORDER BY profit DESC
    """,
        (user_id,),
    )

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


def get_user_by_id(user_id: int):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, email, created_at, password FROM users WHERE id = ?",
        (user_id,),
    )
    user = cursor.fetchone()
    conn.close()
    return user


def update_user_name(user_id: int, name: str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET name = ? WHERE id = ?", (name, user_id))
    conn.commit()
    conn.close()


def update_user_password(user_id: int, hashed_password: str):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password = ? WHERE id = ?", (hashed_password, user_id)
    )
    conn.commit()
    conn.close()
