import httpx
from services.recipe_service import generar_receta, generar_lista_compras

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"
INVENTORY_URL = "http://127.0.0.1:8000/inventory"

async def obtener_inventario() -> list[str]:
    """Obtiene ingredientes desde la API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(INVENTORY_URL)
        response.raise_for_status()
        data = response.json()
        return [item["nombre"] for item in data.get("inventory", [])]

async def consultar_llm(mensaje: str) -> str:
    """
    Recibe el mensaje del usuario, detecta la intención
    y delega a recipe_service o responde directamente.
    """
    texto = mensaje.lower().strip()

    # RECETA
    if any(p in texto for p in ["receta", "comer", "cocinar", "qué hago", "que hago",
                                  "qué puedo", "que puedo", "prepara", "hazme", "sugiere",
                                  "ramen", "pasta", "sopa", "ensalada", "desayuno",
                                  "comida", "cena", "almuerzo"]):
        return await generar_receta(mensaje)

    # LISTA DE COMPRAS
    if any(p in texto for p in ["compras", "lista", "falta", "necesito comprar",
                                  "qué falta", "que falta", "qué me falta", "que me falta"]):
        return await generar_lista_compras(mensaje)

    # INVENTARIO
    if texto == "inventario":
        ingredientes = await obtener_inventario()
        if not ingredientes:
            return "❌ El inventario está vacío."
        return "🥫 *Inventario actual:*\n\n" + "\n".join([f"• {p}" for p in ingredientes])

    # AYUDA / HOLA
    if any(p in texto for p in ["hola", "ayuda", "help", "inicio", "menu", "menú"]):
        return (
            "👋 *Hola! Soy el asistente de tu alacena inteligente* 🥫\n\n"
            "*Comandos disponibles:*\n\n"
            "📋 *inventario* — ver productos disponibles\n"
            "🍽️ *receta* — sugerir receta con lo que tienes\n"
            "🛒 *compras* — lista de lo que te falta comprar\n\n"
            "_También puedes pedirme recetas específicas, por ejemplo:_\n"
            "_'Dame una receta de pasta' o 'Qué puedo cenar hoy'_"
        )

    # CUALQUIER OTRO MENSAJE → LLM con inventario
    ingredientes = await obtener_inventario()
    prompt = (
        f"Eres el asistente de una alacena inteligente. "
        f"Inventario actual: {', '.join(ingredientes)}. "
        f"El usuario dice: '{mensaje}'. "
        f"Responde útil, amigable, máximo 100 palabras en español."
    )

    print(f"🤖 Consultando LLM con modelo {MODEL}...")
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 200,
                "repeat_penalty": 1.1
            }
        })
        response.raise_for_status()
        return response.json().get("response", "").strip()