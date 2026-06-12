import sqlite3


DATABASE_PATH = "nutripantry.db"


def get_connection():

    conn = sqlite3.connect(
        DATABASE_PATH
    )

    conn.row_factory = sqlite3.Row

    return conn