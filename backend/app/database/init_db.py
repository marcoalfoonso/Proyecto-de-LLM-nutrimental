from app.database.database import get_connection

def initialize_database():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        whatsapp_number TEXT UNIQUE,

        name TEXT,

        age INTEGER,

        sex TEXT,

        weight REAL,

        height REAL,

        activity_level TEXT,

        goal TEXT,

        dietary_restrictions TEXT,

        food_preferences TEXT,

        budget REAL
    )
    """)

    conn.commit()

    conn.close()


if __name__ == "__main__":

    initialize_database()

    print(
        "Base de datos inicializada"
    )