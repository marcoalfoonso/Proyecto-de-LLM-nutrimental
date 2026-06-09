import httpx

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"
INVENTORY_URL = "http://127.0.0.1:8000/inventory/db"

async def obtener_inventario() -> list[str]:
    """Obtiene la lista de ingredientes desde la API de inventario."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(INVENTORY_URL)
        response.raise_for_status()
        data = response.json()
        ingredientes = [item["name"] for item in data.get("inventory", [])]
        print(f"🥫 Inventario obtenido: {len(ingredientes)} productos")
        return ingredientes

async def generar_receta(mensaje: str = "") -> str:
    ingredientes = await obtener_inventario()
    if not ingredientes:
        return "❌ No hay ingredientes en el inventario."

    contexto = f"El usuario pide específicamente: '{mensaje}'. Intenta satisfacer esa petición con los ingredientes disponibles. " if mensaje else ""

    prompt = (
        f"Eres el asistente de una alacena inteligente. "
        f"{contexto}"
        f"El usuario tiene estos ingredientes disponibles: {', '.join(ingredientes)}. "
        f"Sugiere UNA receta creativa y variada usando algunos de esos ingredientes. "
        f"Cada vez que respondas, sugiere una receta diferente. "
        f"Responde en español, amigable, máximo 150 palabras. "
        f"Incluye: nombre de la receta, ingredientes a usar y pasos resumidos."
    )

    print("🤖 Generando receta con LLM...")
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.9, "top_p": 0.95, "num_predict": 200, "repeat_penalty": 1.3}
        })
        response.raise_for_status()
        return response.json().get("response", "").strip()

async def generar_lista_compras(mensaje: str = "") -> str:
    ingredientes = await obtener_inventario()
    if not ingredientes:
        return "❌ No hay ingredientes en el inventario."

    contexto = f"El usuario quiere hacer: '{mensaje}'. Considera eso para sugerir qué comprar. " if mensaje else ""

    prompt = (
        f"Eres el asistente de una alacena inteligente. "
        f"{contexto}"
        f"El usuario actualmente tiene: {', '.join(ingredientes)}. "
        f"Basándote en una dieta balanceada y en lo que ya tiene, "
        f"sugiere una lista de compras de máximo 10 productos que le harían falta. "
        f"Responde en español, en formato de lista con viñetas. "
        f"Sé breve y práctico."
    )

    print("🛒 Generando lista de compras con LLM...")
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.5, "top_p": 0.9, "num_predict": 200, "repeat_penalty": 1.1}
        })
        response.raise_for_status()
        return response.json().get("response", "").strip()