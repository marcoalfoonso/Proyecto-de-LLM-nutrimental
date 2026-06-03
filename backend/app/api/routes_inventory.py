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

router = APIRouter()
inventory_service = InventoryService()

@router.get("/inventory")
async def get_inventory():

    inventory = inventory_service.load_inventory()

    return {
        "inventory": inventory
    }