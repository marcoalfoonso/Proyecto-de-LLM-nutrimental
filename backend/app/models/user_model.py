from pydantic import BaseModel

class User(BaseModel):

    usuario_id: str

    nombre: str

    edad: int

    peso: float

    altura: float

    objetivo: str