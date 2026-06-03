from pathlib import Path

class InventoryService:

    def load_inventory(self):

        path = Path('C:\\Users\\Usuario\\Documents\\Prospectiva tecnológica\\Proyecto-de-LLM-nutrimental\\backend\\app\\data\\inventario.txt')

        inventory = []

        with open(path, "r") as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                name, quantity = line.split(",")

                inventory.append({

                    "name": name,
                    "quantity": int(quantity)

                })

        return inventory