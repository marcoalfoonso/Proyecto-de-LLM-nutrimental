import sys
import os

# 1. Get the path of the current file (main.py)
current_dir = os.path.dirname(os.path.abspath(__file__))

# 2. Get the path of the parent directory (my_project)
parent_dir = os.path.dirname(current_dir)

# 3. Add the parent directory to Python's search path
sys.path.append(parent_dir)

from services.inventory_service import InventoryService
from fastapi import APIRouter
from models.inventory_model import InventoryItem

router = APIRouter()
inventory_service = InventoryService()

#endpoint para obtener el inventario, llama a la función load_inventory del servicio de inventario y devuelve el 
# resultado como un diccionario con la clave "inventory" y el valor del inventario cargado

@router.get("/inventory")
async def get_inventory():

    inventory = inventory_service.load_inventory()

    return {
        "inventory": inventory
    }


@router.post("/inventory/add")
async def add_inventory_item(item: InventoryItem):
    inventory_service.add_food(item.nombre, item.cantidad, item.fuente)

    return {
        "message": "Alimento agregado al inventario"
    }


@router.get("/inventory/db")
async def get_inventory_from_db():
    inventory = inventory_service.load_inventory_from_db()
    return {
         "inventory": inventory
    }