from pydantic import BaseModel
from models.Endereco import Endereco
from typing import List

class ListaDeEnderecoDoUsuario(BaseModel):
    id_usuario: int
    endereco: List[Endereco] = []