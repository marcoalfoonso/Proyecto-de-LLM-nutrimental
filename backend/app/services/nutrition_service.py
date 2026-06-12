from models.user_profile import UserProfile
from models.nutrition_profile import NutritionProfile


class NutritionService:

    ACTIVITY_FACTORS = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9
    }

    def calculate_bmi(
        self,
        weight: float,
        height_cm: float
    ) -> float:

        height_m = height_cm / 100

        return round(
            weight / (height_m ** 2),
            2
        )

    def calculate_tmb(
        self,
        user: UserProfile
    ) -> float:

        if user.sex.lower() == "male":

            return (
                (10 * user.weight)
                +
                (6.25 * user.height)
                -
                (5 * user.age)
                +
                5
            )

        return (
            (10 * user.weight)
            +
            (6.25 * user.height)
            -
            (5 * user.age)
            -
            161
        )

    def calculate_get(
        self,
        tmb: float,
        activity_level: str
    ) -> float:

        factor = self.ACTIVITY_FACTORS.get(
            activity_level,
            1.2
        )

        return tmb * factor

    def calculate_calorie_target(
        self,
        get: float,
        goal: str
    ) -> float:

        if goal == "weight_loss":
            return get * 0.85

        if goal == "muscle_gain":
            return get * 1.10

        if goal == "recomposition":
            return get * 0.95

        return get

    def calculate_macros(
        self,
        calories: float,
        weight: float,
        goal: str
    ):

        if goal == "muscle_gain":

            protein = weight * 2.0

        elif goal == "weight_loss":

            protein = weight * 2.2

        else:

            protein = weight * 1.8

        fat = weight * 0.8

        protein_calories = protein * 4

        fat_calories = fat * 9

        carb_calories = (
            calories
            -
            protein_calories
            -
            fat_calories
        )

        carbs = carb_calories / 4

        return (
            round(protein),
            round(fat),
            round(carbs)
        )

    def generate_profile(
        self,
        user: UserProfile
    ) -> NutritionProfile:

        tmb = self.calculate_tmb(user)

        get = self.calculate_get(
            tmb,
            user.activity_level
        )

        calories_target = (
            self.calculate_calorie_target(
                get,
                user.goal
            )
        )

        protein, fat, carbs = (
            self.calculate_macros(
                calories_target,
                user.weight,
                user.goal
            )
        )

        return NutritionProfile(
            tmb=round(tmb),
            get=round(get),
            calories_target=round(
                calories_target
            ),
            protein_target=protein,
            fat_target=fat,
            carb_target=carbs
        )