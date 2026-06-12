from dataclasses import dataclass

from models.recipe import Recipe


@dataclass
class Meal:

    recipe: Recipe

    meal_type: str