from connection import get_connection

conn = get_connection()
cursor = conn.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS inventory(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    quantity INTEGER NOT NULL,
    source TEXT,
    last_update DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
               usuario_id INTEGER PRIMARY KEY AUTOINCREMENT,
               nombre TEXT NOT NULL,
               edad INTEGER NOT NULL,
               peso REAL NOT NULL,
               altura REAL NOT NULL,
               objetivo TEXT NOT NULL,
               ultima_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
               )
               """)

conn.commit()

conn.close()

print("Database created")
