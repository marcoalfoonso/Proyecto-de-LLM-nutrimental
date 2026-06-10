from database.connection import get_connection


class UsersService:

    #funcion para consultar usuarios

    def load_users(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users")

        users = cursor.fetchall()

        conn.close()

        return [dict(users) for users in users]
    
    def add_user(self,nombre,edad,peso,altura,objetivo):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users(nombre,edad,peso,altura,objetivo)
            VALUES(?,?,?,?,?)

            ON CONFLICT(nombre)
            DO NOTHING
            """,
            (nombre,edad,peso,altura,objetivo)
        )

        conn.commit()
        conn.close()