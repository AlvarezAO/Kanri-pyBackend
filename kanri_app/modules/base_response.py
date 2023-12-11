from pydantic import BaseModel
from datetime import datetime

class StandardResponse(BaseModel):
    mensaje: str = "Se ha ejecutado."
    estado: str = "OK"
    codigo: int = 200
    fecha: datetime = datetime.now()