import sys
from services.database import connect, migrate_crops_table
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


conn = connect()
cursor = conn.cursor()
cursor.execute("PRAGMA database_list")
print("Database file:", cursor.fetchall())
conn.close()

print("Running migration...")
migrate_crops_table()
print("Done.")
