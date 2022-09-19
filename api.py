from models.Usuario import Usuario
from models.Endereco import Endereco
from models.ListaDeEnderecosDoUsuario import ListaDeEnderecoDoUsuario
from models.Produto import Produto
from models.CarrinhoDeCompras import CarrinhoDeCompras
from fastapi import FastAPI

app = FastAPI()
OK = "OK"
FALHA = "FALHA"

db_usuarios = {}
db_produtos = {}
db_endereco = []       
db_carrinhos = []


def cadastro_usuario(usuario: Usuario):
    db_usuarios[usuario.id] = usuario
    db_endereco.append(ListaDeEnderecoDoUsuario(id_usuario=usuario.id))
    db_carrinhos.append(CarrinhoDeCompras(id_usuario=usuario.id, preco_total=0.00, qtdd_produtos=0))
    return OK

def validar_cadastro(usuario: Usuario):
    if len(usuario.senha) < 3 or '@' not in usuario.email:
        return FALHA
    return cadastro_usuario(usuario)

def excluir_usuario(id: int):
    del db_usuarios[id]

def excluir_endereco(id: int):
    for end in db_endereco:
        if end.id_usuario == id:
            db_endereco.remove(end)
        continue

def excluir_carrinho(id: int):
    for cart in db_carrinhos:
        if cart.id_usuario == id:
            db_carrinhos.remove(cart)
        continue
    
def buscar_usuario_endereco(id_usuario: int):
    return list(filter(lambda end: end.id_usuario == id_usuario, db_endereco))

def index_endereco(id_usuario: int):
    end = buscar_usuario_endereco(id_usuario)
    return db_endereco.index(end[0])

def buscar_index_endereco(id_endereco: int):
    for end in db_endereco:
        for e in end.endereco:
            if (e.id == id_endereco):
                return {'index_endereco': db_endereco.index(end),'index_endereco': end.endereco.index(e)}
                
def buscar_index_carrinho(id_usuario: int):
    for car in db_carrinhos:
        if car.id_usuario == id_usuario:
            return db_carrinhos.index(car)

def verificar_carrinho(id_usuario: int):
    i = buscar_index_carrinho(id_usuario)
    if i is None:
        db_carrinhos.append(CarrinhoDeCompras(id_usuario=id_usuario, preco_total=0.00, qtdd_produtos=0))

def add_produto_ao_carrinho(id_usuario: int, id_produto: int):
    i = buscar_index_carrinho(id_usuario)
    cart = db_carrinhos[i]
    prod = db_produtos[id_produto]
    cart.qtdd_produtos += 1
    cart.id_produtos.append(prod)
    cart.preco_total += prod.preco
    db_carrinhos[i] = CarrinhoDeCompras(preco_total=cart.preco_total, id_usuario=id_usuario, 
                                        qtdd_produtos=cart.qtdd_produtos, id_produtos=cart.id_produtos)
    
def remover_produto_do_carrinho(id_produto: int):
    for cart in db_carrinhos:
        for prod in cart.id_produtos:
            if (prod.id == id_produto):
                i_carrinho = db_carrinhos.index(cart)
                index_produtos = cart.id_produtos.index(prod)
                db_carrinhos[i_carrinho].id_produtos.pop(index_produtos)
                db_carrinhos[i_carrinho].preco_total -= prod.preco
                db_carrinhos[i_carrinho].qtdd_produtos -= 1


@app.post("/usuario/")
async def criar_usuario(usuario: Usuario):
    if usuario.id in db_usuarios:
        return FALHA
    return validar_cadastro(usuario)

@app.get("/usuario/")
async def retornar_usuario(id: int):
    if id in db_usuarios:
        return db_usuarios[id]
    return FALHA

@app.get("/usuario/nome")
async def retornar_usuario_nome(nome: str):
    resultado = []
    for item in db_usuarios.values():
        nome_pesquisado = item.nome.split()[0].upper()
        if nome_pesquisado == nome.upper():
            resultado.append(item)
        continue
    return resultado if len(resultado) else FALHA

@app.delete("/usuario/")
async def deletar_usuario(id: int):
    if id in db_usuarios:
        excluir_usuario(id)
        excluir_endereco(id)
        excluir_carrinho(id)
        return OK
    return FALHA

@app.get("/usuario/{id_usuario}/enderecos/")
async def retornar_endereco_do_usuario(id_usuario: int):
    if id_usuario not in db_usuarios:
        return FALHA
    else:
        end = buscar_usuario_endereco(id_usuario)
        return end[0].endereco

@app.post("/endereco/{id_usuario}/")
async def criar_endereco(endereco: Endereco, id_usuario: int):
    if id_usuario not in db_usuarios:
        return FALHA
    else:
        index = index_endereco(id_usuario)
        end = db_endereco[index].endereco
        end.append(endereco)
        db_endereco[index].endereco = end
        return OK

@app.delete("/endereco/{id_endereco}/")
async def deletar_endereco(id_endereco: int):
    i = buscar_index_endereco(id_endereco)
    if not i:
        return FALHA
    db_endereco[i["index_endereco"]].endereco.pop(i["index_endereco"])
    return OK

@app.post("/produto/")
async def criar_produto(produto: Produto):
    if produto.id in db_produtos:
        return FALHA
    db_produtos[produto.id] = produto
    return OK

@app.get("/produto/{id_produto}/")
async def criar_produto(id_produto: int):
    if id_produto not in db_produtos:
        return FALHA
    return db_produtos[id_produto]

@app.delete("/produto/{id_produto}/")
async def deletar_produto(id_produto: int):
    if id_produto not in db_produtos:
        return FALHA
    remover_produto_do_carrinho(id_produto)
    db_produtos.pop(id_produto)
    return OK

@app.post("/carrinho/{id_usuario}/{id_produto}/")
async def adicionar_carrinho(id_usuario: int, id_produto: int):
    if id_usuario not in db_usuarios or id_produto not in db_produtos:
        return FALHA
    verificar_carrinho(id_usuario)
    add_produto_ao_carrinho(id_usuario, id_produto)
    return OK

@app.get("/carrinho/{id_usuario}/info")
async def retornar_carrinho(id_usuario: int):
    index = buscar_index_carrinho(id_usuario)
    if index is None:
        return FALHA
    return db_carrinhos[index]

@app.get("/carrinho/{id_usuario}/")
async def retornar_total_carrinho(id_usuario: int):
    index = buscar_index_carrinho(id_usuario)
    if index is None:
        return FALHA
    return f'numero itens: {db_carrinhos[index].qtdd_produtos} | valor_total: {db_carrinhos[index].preco_total}'

@app.delete("/carrinho/{id_usuario}/")
async def deletar_carrinho(id_usuario: int):
    if not id_usuario in db_usuarios:
        return FALHA
    index = buscar_index_carrinho(id_usuario)
    if index is None:
        return OK
    db_carrinhos.pop(index)
    return OK

@app.get("/")
async def bem_vinda():
    site = "Seja bem vindo(a)!"
    return site.replace('\n', '')