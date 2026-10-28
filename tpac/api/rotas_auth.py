from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from controllers.usuario_controller import login_api

router = APIRouter(
    tags=["auth"]
)


class LoginRequest(BaseModel):
    email: str
    senha: str


@router.post("/login")
def login(dados: LoginRequest):
    try:
        resultado = login_api(dados.email, dados.senha)
    except ValueError as erro:
        raise HTTPException(status_code=401, detail=str(erro))

    return resultado