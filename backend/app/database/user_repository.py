import json

from app.database.database import (
    get_connection
)

from app.models.user_profile import (
    UserProfile
)


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

    def get_by_whatsapp(
        self,
        whatsapp_number: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE whatsapp_number = ?
            """,
            (whatsapp_number,)
        )

        row = cursor.fetchone()

        conn.close()

        if not row:
            return None

        return UserProfile(

            id=row["id"],

            name=row["name"],

            age=row["age"],

            sex=row["sex"],

            weight=row["weight"],

            height=row["height"],

            activity_level=row[
                "activity_level"
            ],

            goal=row["goal"],

            dietary_restrictions=
                json.loads(
                    row[
                        "dietary_restrictions"
                    ]
                    or "[]"
                ),

            food_preferences=
                json.loads(
                    row[
                        "food_preferences"
                    ]
                    or "[]"
                ),

            budget=row["budget"]
        )

    def update(
        self,
        user: UserProfile,
        whatsapp_number: str
    ):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE users
            SET

                name=?,

                age=?,

                sex=?,

                weight=?,

                height=?,

                activity_level=?,

                goal=?,

                dietary_restrictions=?,

                food_preferences=?,

                budget=?

            WHERE whatsapp_number=?
            """,
            (

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

                user.budget,

                whatsapp_number
            )
        )

        conn.commit()

        conn.close()