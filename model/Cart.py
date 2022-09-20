from pydantic import BaseModel
from typing import List

class Usuario(BaseModel):
    id: int
    nome: str
    email: str
    senha: str
    
class Endereco(BaseModel):
    id: int
    rua: str
    cep: str
    cidade: str
    estado: str
    
class ListaDeEnderecoDoUsuario(BaseModel):
    id_usuario: int
    endereco: List[Endereco] = []

class Produto(BaseModel):
    id: int
    nome: str
    descricao: str
    preco: float
    
class CarrinhoDeCompras(BaseModel):
    id_usuario: int
    id_produtos: List[Produto] = []
    preco_total: float
    qtdd_produtos: int