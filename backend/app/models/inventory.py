from dataclasses import dataclass, field

from models.ingredient import Ingredient


@dataclass
class Inventory:

    user_id: int

    ingredients: list[Ingredient] = field(
        default_factory=list
    )