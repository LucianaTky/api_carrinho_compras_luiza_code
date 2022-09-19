from pydantic import BaseModel

class Endereco(BaseModel):
    id: int
    rua: str
    cep: str
    cidade: str
    estado: str