import json
from pathlib import Path

class InventoryService:

    def load_inventory(self):

        path = Path('C:\\Users\\Usuario\\Documents\\Prospectiva tecnológica\\Proyecto-de-LLM-nutrimental\\backend\\app\\data\\inventario.json')

        with open(path, "r") as file:

            inventory = json.load(file)
            return inventory