from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from controllers.usuario_controller import listar_usuarios_api, criar_usuario_api, buscar_usuario_api, atualizar_usuario_api, excluir_usuario_api
from auth_token import verificar_token

security = HTTPBearer()

router = APIRouter(
    prefix="/usuarios",
    tags=["usuarios"]
)


class NovoUsuario(BaseModel):
    nome: str
    email: str
    senha: str
    estilo_instrucao: str = "direto"


@router.get("")
def listar_usuarios(
    busca: str = None,
    limite: int = None,
    token = Depends(verificar_token)
):
    print("Usuário atual:", token)

    return {
        "dados": listar_usuarios_api(busca=busca, limite=limite)
    }

@router.post("", status_code=status.HTTP_201_CREATED)
def criar_usuario(dados: NovoUsuario):
    try:
        usuario = criar_usuario_api(
            dados.nome,
            dados.email,
            dados.senha,
            dados.estilo_instrucao
        )
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))

    return {"dados": usuario}


@router.get("/{usuario_id}")
def buscar_usuario(usuario_id: int):
    try:
        usuario = buscar_usuario_api(usuario_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

    return {"dados": usuario}

class AtualizarUsuario(BaseModel):
    email: str
    estilo_instrucao: str = "direto"


@router.get("/{usuario_id}")
def buscar_usuario(usuario_id: int):
    try:
        usuario = buscar_usuario_api(usuario_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

    return {"dados": usuario}


@router.put("/{usuario_id}")
def atualizar_usuario(usuario_id: int, dados: AtualizarUsuario):
    try:
        usuario = atualizar_usuario_api(usuario_id, dados.email, dados.estilo_instrucao)
    except ValueError as erro:
        status_code = 404 if erro.args[0] == "Usuário não encontrado." else 422
        raise HTTPException(status_code=status_code, detail=str(erro))

    return {"dados": usuario}

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_usuario(usuario_id: int, token = Depends(verificar_token)):
    if token["papel"] != "admin":
        raise HTTPException(status_code=403, detail="Apenas administradores podem excluir usuários.")

    try:
        excluir_usuario_api(usuario_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))