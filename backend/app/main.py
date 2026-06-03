from api.routes_inventory import router as inventory_router
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "backend funcionando"}


app.include_router(inventory_router)