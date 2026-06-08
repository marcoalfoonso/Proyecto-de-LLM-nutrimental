from api.routes_inventory import router as inventory_router
from api.routes_chat import router as chat_router
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "backend funcionando"}

app.include_router(inventory_router)
app.include_router(chat_router)