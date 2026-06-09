import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import consultar_llm

router = APIRouter()
historial = []

class MensajeEntrada(BaseModel):
    numero: str
    mensaje: str

class RespuestaChat(BaseModel):
    numero: str
    respuesta: str

@router.post("/chat", response_model=RespuestaChat)
async def recibir_mensaje(entrada: MensajeEntrada):
    print(f"\n📩 Mensaje de {entrada.numero}: {entrada.mensaje}")

    if not entrada.mensaje.strip():
        raise HTTPException(status_code=400, detail="Mensaje vacío")

    respuesta = await consultar_llm(entrada.mensaje)
    print(f"✅ Respuesta: {respuesta}")

    # Guardar mensaje Y respuesta en historial
    historial.append({
        "numero": entrada.numero,
        "mensaje": entrada.mensaje,
        "respuesta": respuesta
    })
    print(f"📋 Historial: {len(historial)} mensajes")

    return RespuestaChat(numero=entrada.numero, respuesta=respuesta)

@router.get("/chat/historial")
async def ver_historial():
    return {"total": len(historial), "mensajes": historial}

@router.get("/chat/health")
async def health():
    return {"status": "ok", "servicio": "chat"}