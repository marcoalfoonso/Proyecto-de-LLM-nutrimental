from services.nutrition_service import (
    NutritionService
)

from models.user_profile import (
    UserProfile
)


user = UserProfile(
    id=1,
    name="Renata",
    age=22,
    sex="female",
    weight=60,
    height=165,
    activity_level="moderate",
    goal="muscle_gain",
    dietary_restrictions=[],
    food_preferences=[]
)

nutrition = NutritionService()

profile = nutrition.generate_profile(
    user
)

print(profile)