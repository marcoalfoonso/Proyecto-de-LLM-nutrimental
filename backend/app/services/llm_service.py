import httpx
from services.recipe_service import generar_receta, generar_lista_compras

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:3b"
INVENTORY_URL = "http://127.0.0.1:8000/inventory"
INVENTORY_ADD_URL = "http://127.0.0.1:8000/inventory/add"

async def obtener_inventario() -> list[str]:
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(INVENTORY_URL)
        response.raise_for_status()
        data = response.json()
        return [item["nombre"] for item in data.get("inventory", [])]

async def agregar_producto(nombre: str, cantidad: int = 1) -> bool:
    """Agrega un producto al inventario via API."""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(INVENTORY_ADD_URL, json={
                "nombre": nombre.strip(),
                "cantidad": cantidad,
                "fuente": "whatsapp"
            })
            response.raise_for_status()
            print(f"✅ Producto agregado: {nombre} (x{cantidad})")
            return True
    except Exception as e:
        print(f"❌ Error agregando {nombre}: {e}")
        return False

async def extraer_productos_con_llm(mensaje: str) -> list[dict]:
    """
    Usa el LLM para extraer productos y cantidades del mensaje.
    Devuelve lista de dicts: [{"nombre": "pollo", "cantidad": 1}, ...]
    """
    prompt = (
        f"El usuario dice: '{mensaje}'. "
        f"Extrae todos los productos o alimentos que menciona con su cantidad. "
        f"Responde SOLO en este formato, uno por línea: nombre,cantidad. "
        f"Ejemplo: pollo,1 / zanahorias,3 / leche,2. "
        f"Si no se menciona cantidad, usa 1. "
        f"Solo nombres simples en minúsculas, sin artículos (no 'un pollo', solo 'pollo'). "
        f"No agregues explicaciones ni texto extra."
    )

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(OLLAMA_URL, json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": 60,
            }
        })
        response.raise_for_status()
        texto = response.json().get("response", "").strip()

    productos = []
    for linea in texto.split("\n"):
        linea = linea.strip().replace("- ", "").replace("* ", "")
        if "," in linea:
            partes = linea.split(",")
            nombre = partes[0].strip().lower()
            try:
                cantidad = int(partes[1].strip())
            except:
                cantidad = 1
            if nombre:
                productos.append({"nombre": nombre, "cantidad": cantidad})

    return productos

async def consultar_llm(mensaje: str) -> str:
    texto = mensaje.lower().strip()

    # AGREGAR PRODUCTO AL INVENTARIO
    palabras_agregar = [
        "agregué", "agregue", "agregando", "agregar",
        "compré", "compre", "comprando", "comprar",
        "conseguí", "consegui", "añadí", "anadí",
        "traje", "llegó", "llego", "acabo de comprar",
        "acabo de traer", "ya tengo", "me traje", "tengo"
    ]
    if any(p in texto for p in palabras_agregar):
        productos = await extraer_productos_con_llm(mensaje)
        if not productos:
            return "❌ No pude identificar los productos. Intenta con: 'agregué [producto]'"

        confirmados = []
        for p in productos:
            exito = await agregar_producto(p["nombre"], p["cantidad"])
            if exito:
                confirmados.append(f"• {p['nombre']} (x{p['cantidad']})")

        if confirmados:
            return "✅ *Productos agregados a tu alacena:*\n\n" + "\n".join(confirmados)
        return "❌ No se pudo agregar ningún producto."

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
            "_'Agregué una piña y 3 zanahorias'_\n"
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