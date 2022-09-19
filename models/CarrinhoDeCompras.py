from pydantic import BaseModel
from models.Produto import Produto
from typing import List

class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: List[Produto] = []
    preco_total: float
    qtdd_produtos: int