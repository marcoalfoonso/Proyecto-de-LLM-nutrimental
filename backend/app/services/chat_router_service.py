class ChatRouterService:

    def classify(
        self,
        message: str
    ) -> str:

        text = message.lower()

        if any(
            p in text
            for p in [
                "inventario",
                "qué tengo",
                "que tengo"
            ]
        ):
            return "inventory"

        if any(
            p in text
            for p in [
                "receta",
                "cocinar",
                "qué puedo cocinar",
                "que puedo cocinar"
            ]
        ):
            return "recipe"

        if any(
            p in text
            for p in [
                "compras",
                "qué falta",
                "que falta"
            ]
        ):
            return "shopping"

        if any(
            p in text
            for p in [
                "dieta",
                "plan semanal",
                "meal plan"
            ]
        ):
            return "meal_plan"

        return "general"