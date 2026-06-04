import json
from pathlib import Path

class InventoryService:

    def load_inventory(self):

        path = (
            Path(__file__).resolve().parent.parent
            / "data"
            / "inventario.json"
        )

        with open(path, "r",encoding="utf-8") as file:

            inventory = json.load(file)
            return inventory