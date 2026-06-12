import json

from app.database.database import get_connection

from models.user_profile import UserProfile


class UserRepository:

    def create(
        self,
        user: UserProfile,
        whatsapp_number: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users (

                whatsapp_number,

                name,

                age,

                sex,

                weight,

                height,

                activity_level,

                goal,

                dietary_restrictions,

                food_preferences,

                budget

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                whatsapp_number,

                user.name,

                user.age,

                user.sex,

                user.weight,

                user.height,

                user.activity_level,

                user.goal,

                json.dumps(
                    user.dietary_restrictions
                ),

                json.dumps(
                    user.food_preferences
                ),

                user.budget
            )
        )

        conn.commit()

        conn.close()