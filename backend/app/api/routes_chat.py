from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ─── MODELOS DE DATOS ─────────────────────────────────────────────

class MensajeEntrada(BaseModel):
    """Mensaje que llega desde index.js (WhatsApp)"""
    numero: str       # número del usuario ej: "5215512345678"
    mensaje: str      # texto que escribió el usuario

class RespuestaChat(BaseModel):
    """Respuesta que se regresa a index.js"""
    numero: str       # a quién responder
    respuesta: str    # texto generado por el LLM

# ─── RUTA PRINCIPAL ───────────────────────────────────────────────

@router.post("/chat", response_model=RespuestaChat)
async def recibir_mensaje(entrada: MensajeEntrada):
    """
    Recibe un mensaje de WhatsApp desde index.js,
    lo pasa al LLM y regresa la respuesta.
    """
    print(f"\n📩 Mensaje recibido de {entrada.numero}: {entrada.mensaje}")

    if not entrada.mensaje.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")

    # Por ahora responde con eco para probar que la ruta funciona
    # Aquí después conectaremos llm_service.py
    respuesta_prueba = f"[ECHO] Recibí tu mensaje: '{entrada.mensaje}'"

    print(f"✅ Respuesta lista para {entrada.numero}: {respuesta_prueba}")

    return RespuestaChat(
        numero=entrada.numero,
        respuesta=respuesta_prueba
    )

# ─── RUTA DE SALUD ────────────────────────────────────────────────

@router.get("/chat/health")
async def health():
    """Verifica que el servicio de chat esté activo"""
    return {"status": "ok", "servicio": "chat"}