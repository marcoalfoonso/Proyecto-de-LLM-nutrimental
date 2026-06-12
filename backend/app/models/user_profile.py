from dataclasses import dataclass
from typing import Optional


@dataclass
class UserProfile:

    id: int

    name: str

    age: int

    sex: str

    weight: float

    height: float

    activity_level: str

    goal: str

    dietary_restrictions: list[str]

    food_preferences: list[str]

    budget: Optional[float] = None