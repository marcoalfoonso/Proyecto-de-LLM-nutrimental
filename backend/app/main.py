import time
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from api.routes_inventory import router as inventory_router
from api.routes_chat import router as chat_router

app = FastAPI(title="Alacena Inteligente API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(inventory_router)
app.include_router(chat_router)

OLLAMA_CHAT_URL = "http://localhost:11434/api/chat"

# ── ENDPOINT DEL PANEL ADMIN (con métricas) ──────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=4000)
    model: str = Field(default="llama3.2:3b")
    temperature: float = Field(default=0.7, ge=0.0, le=1.2)
    top_p: float = Field(default=0.9, ge=0.1, le=1.0)
    num_predict: int = Field(default=160, ge=20, le=1000)
    num_ctx: int = Field(default=4096, ge=512, le=8192)
    repeat_penalty: float = Field(default=1.1, ge=1.0, le=2.0)
    keep_alive: str = Field(default="5m")
    system_prompt: str = Field(default="Eres el asistente de una alacena inteligente. Ayudas con recetas, inventario y lista de compras. Responde en español.")

@app.post("/chat/admin")
def chat_admin(request: ChatRequest):
    payload = {
        "model": request.model,
        "messages": [
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.message},
        ],
        "stream": False,
        "keep_alive": request.keep_alive,
        "options": {
            "temperature": request.temperature,
            "top_p": request.top_p,
            "num_predict": request.num_predict,
            "num_ctx": request.num_ctx,
            "repeat_penalty": request.repeat_penalty,
        },
    }

    try:
        start = time.perf_counter()
        response = requests.post(OLLAMA_CHAT_URL, json=payload, timeout=300)
        wall = time.perf_counter() - start
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="No se pudo conectar con Ollama.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    ed = data.get("eval_duration", 0) / 1e9
    ec = data.get("eval_count", 0)

    return {
        "model": request.model,
        "reply": data.get("message", {}).get("content", ""),
        "metrics": {
            "wall_time_s": round(wall, 3),
            "total_duration_s": round(data.get("total_duration", 0) / 1e9, 3),
            "load_duration_s": round(data.get("load_duration", 0) / 1e9, 3),
            "prompt_eval_count": data.get("prompt_eval_count", 0),
            "eval_count": ec,
            "total_tokens": data.get("prompt_eval_count", 0) + ec,
            "eval_duration_s": round(ed, 3),
            "tokens_per_second": round(ec / ed if ed > 0 else 0, 2),
        }
    }

@app.get("/")
def root():
    return {"message": "Alacena Inteligente API funcionando"}