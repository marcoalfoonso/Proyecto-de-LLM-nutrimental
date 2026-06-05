import json
from pathlib import Path
from database.connection import get_connection


#lee el archivo json y lo devuelve como un diccionario

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
        

#función que agrega un nuevo alimento a la base de datos, recibe el nombre, cantidad y fuente del alimento como parámetros
        
def add_food(name, quantity, source):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO inventory(name, quantity, source)
        VALUES (?, ?, ?)
        """,
        (name, quantity, source)
    )

    conn.commit()

    conn.close()


#función que carga el inventario desde la base de datos, devuelve una lista de diccionarios con los alimentos y
# sus cantidades, fuentes y fechas de actualización

def load_inventory():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM inventory"
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
