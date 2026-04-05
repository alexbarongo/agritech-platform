import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.database import connect, migrate_crops_table, migrate_expenses_table

conn = connect()
cursor = conn.cursor()
cursor.execute("PRAGMA database_list")
print("Database file:", cursor.fetchall())
conn.close()

print("Running migration...")
migrate_crops_table()
migrate_expenses_table()
print("Done.")
