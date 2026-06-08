from pydantic import BaseModel

class Detection(BaseModel):

    name: str

    confidence: float