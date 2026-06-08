import httpx
from services.recipe_service import generar_receta, generar_lista_compras

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"
INVENTORY_URL = "http://127.0.0.1:8000/inventory"
INVENTORY_ADD_URL = "http://127.0.0.1:8000/inventory/add"

async def obtener_inventario() -> list[str]:
    """Obtiene ingredientes desde la API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(INVENTORY_URL)
        response.raise_for_status()
        data = response.json()
        return [item["nombre"] for item in data.get("inventory", [])]

async def agregar_producto(nombre: str) -> str:
    """Agrega un producto al inventario via API."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(INVENTORY_ADD_URL, json={
            "nombre": nombre,
            "cantidad": 1,
            "fuente": "whatsapp"
        })
        response.raise_for_status()
        print(f"✅ Producto agregado: {nombre}")
        return f"✅ *{nombre}* agregado a tu alacena."

async def extraer_producto_con_llm(mensaje: str) -> str:
    """Usa el LLM para extraer el nombre del producto del mensaje."""
    prompt = (
        f"El usuario dice: '{mensaje}'. "
        f"Extrae SOLO el nombre del producto o alimento que menciona. "
        f"Responde ÚNICAMENTE con el nombre del producto, sin explicaciones, "
        f"sin puntos, sin comillas. Solo el nombre. "
        f"Ejemplo: si dice 'agregué una piña', responde: piña. "
        f"Si dice 'compré leche y huevos', responde solo el primero: leche."
    )

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 20,
            }
        })
        response.raise_for_status()
        producto = response.json().get("response", "").strip().lower()
        # Limpiar respuesta
        producto = producto.replace(".", "").replace('"', "").replace("'", "").strip()
        return producto

async def consultar_llm(mensaje: str) -> str:
    """
    Recibe el mensaje del usuario, detecta la intención
    y delega al servicio correspondiente.
    """
    texto = mensaje.lower().strip()

    # AGREGAR PRODUCTO AL INVENTARIO
    palabras_agregar = [
        "agregué", "agregue", "agregando", "agregar",
        "compré", "compre", "comprando", "comprar",
        "tengo", "conseguí", "consegui", "añadí", "anadí",
        "traje", "llegó", "llego", "acabo de comprar",
        "acabo de traer", "ya tengo", "me traje"
    ]
    if any(p in texto for p in palabras_agregar):
        producto = await extraer_producto_con_llm(mensaje)
        if producto:
            return await agregar_producto(producto)
        return "❌ No pude identificar el producto. Intenta con: 'agregué [producto]'"

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
            "🛒 *compras* — lista de lo que te falta comprar\n"
            "➕ *agregué [producto]* — agregar producto al inventario\n\n"
            "_Ejemplos:_\n"
            "_'Dame una receta de pasta'_\n"
            "_'Agregué una piña'_\n"
            "_'Qué me falta comprar'_"
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