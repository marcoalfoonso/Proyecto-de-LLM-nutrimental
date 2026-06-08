from connection import get_connection

conn = get_connection()
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    quantity INTEGER NOT NULL,
    source TEXT,
    last_update DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

conn.close()

print("Database created")
