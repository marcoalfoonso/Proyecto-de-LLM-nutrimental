from pydantic import BaseModel, Field

class InventoryItem(BaseModel):

    nombre: str = Field(
        min_length=2,
        max_length=50
    )

    cantidad: int = Field(
        gt=0
    )

    fuente: str = "user"