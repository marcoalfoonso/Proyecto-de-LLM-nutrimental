from pydantic import BaseModel

class Meal(BaseModel):

    nombre_comida: str

    calorias: int

    proteina: float

    carbos: float

    grasa: float