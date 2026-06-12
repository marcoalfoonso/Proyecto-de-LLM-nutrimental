from dataclasses import dataclass, field

from models.meal import Meal


@dataclass
class DailyPlan:

    breakfast: Meal

    lunch: Meal

    dinner: Meal

    snacks: list[Meal] = field(
        default_factory=list
    )


@dataclass
class MealPlan:

    days: dict[str, DailyPlan]