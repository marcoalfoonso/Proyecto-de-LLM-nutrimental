from app.models.recipe import Recipe
from app.models.meal import Meal
from app.models.meal_plan import (
    DailyPlan,
    MealPlan
)

from app.models.enums import Goal


class MealPlanService:

    def generate_meal_plan(
        self,
        calories_target: float,
        goal: str
    ) -> MealPlan:

        if goal == Goal.MUSCLE_GAIN:

            breakfast_pct = 0.25
            lunch_pct = 0.30
            dinner_pct = 0.25
            snack_pct = 0.20

        else:

            breakfast_pct = 0.25
            lunch_pct = 0.35
            dinner_pct = 0.30
            snack_pct = 0.10

        breakfast_recipe = Recipe(
            name="Desayuno balanceado",
            description="Desayuno sugerido",
            calories=round(calories_target * breakfast_pct)
        )

        lunch_recipe = Recipe(
            name="Comida balanceada",
            description="Comida sugerida",
            calories=round(calories_target * lunch_pct)
        )

        dinner_recipe = Recipe(
            name="Cena balanceada",
            description="Cena sugerida",
            calories=round(calories_target * dinner_pct)
        )

        snack_recipe = Recipe(
            name="Snack saludable",
            description="Snack sugerido",
            calories=round(calories_target * snack_pct)
        )

        breakfast = Meal(
            recipe=breakfast_recipe,
            meal_type="breakfast"
        )

        lunch = Meal(
            recipe=lunch_recipe,
            meal_type="lunch"
        )

        dinner = Meal(
            recipe=dinner_recipe,
            meal_type="dinner"
        )

        snack = Meal(
            recipe=snack_recipe,
            meal_type="snack"
        )

        day = DailyPlan(
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snacks=[snack]
        )

        return MealPlan(
            days={
                "monday": day,
                "tuesday": day,
                "wednesday": day,
                "thursday": day,
                "friday": day,
                "saturday": day,
                "sunday": day
            }
        )