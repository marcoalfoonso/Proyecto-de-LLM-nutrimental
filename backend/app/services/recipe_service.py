from app.services.inventory_service import (
    InventoryService
)

from app.services.nutrition_service import (
    NutritionService
)

from app.services.llm_service import (
    LLMService
)

from app.database.user_repository import (
    UserRepository
)

from app.utils.prompt_manager import (
    PromptManager
)


class RecipeService:

    def __init__(self):

        self.inventory_service = (
            InventoryService()
        )

        self.user_repository = (
            UserRepository()
        )

        self.nutrition_service = (
            NutritionService()
        )

        self.llm_service = (
            LLMService()
        )

    async def generate_recipe(
        self,
        whatsapp_number: str
    ) -> str:

        user = (
        self.user_repository
        .get_by_whatsapp(
            whatsapp_number
        )
)

        if not user:

            return (
                "No existe perfil nutricional "
                "para este usuario."
            )

        inventory = (
            self.inventory_service
            .load_inventory_from_db()
        )

        nutrition = (
            self.nutrition_service
            .generate_profile(user)
        )

        base_prompt = (
            PromptManager.load(
                "recipe_prompt.txt"
            )
        )

        inventory_text = "\n".join([
            f"- {item['name']} "
            f"(x{item['quantity']})"
            for item in inventory
        ])

        final_prompt = f"""
{base_prompt}

PERFIL DEL USUARIO

Edad: {user.age}
Sexo: {user.sex}
Peso: {user.weight}
Altura: {user.height}
Objetivo: {user.goal}

OBJETIVOS NUTRICIONALES

Calorías: {nutrition.calories_target}
Proteínas: {nutrition.protein_target}
Carbohidratos: {nutrition.carb_target}
Grasas: {nutrition.fat_target}

INVENTARIO DISPONIBLE

{inventory_text}
"""

        response = await (
            self.llm_service.generate(
                prompt=final_prompt,
                temperature=0.3,
                max_tokens=800
            )
        )

        return response.content