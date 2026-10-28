from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from controllers.tarefa_controller import listar_tarefas_api, criar_tarefa_api, alternar_status_api, excluir_tarefa_api

router = APIRouter(
    tags=["tarefas"]
)


class NovaTarefa(BaseModel):
    tipo: str
    titulo: str


@router.get("/usuarios/{usuario_id}/tarefas")
def listar_tarefas_do_usuario(usuario_id: int):
    return {
        "dados": listar_tarefas_api(usuario_id)
    }


@router.post("/usuarios/{usuario_id}/tarefas", status_code=status.HTTP_201_CREATED)
def criar_tarefa(usuario_id: int, dados: NovaTarefa):
    try:
        tarefa = criar_tarefa_api(usuario_id, dados.tipo, dados.titulo)
    except ValueError as erro:
        raise HTTPException(status_code=422, detail=str(erro))

    return {"dados": tarefa}


@router.patch("/usuarios/{usuario_id}/tarefas/{tarefa_id}")
def alternar_status_tarefa(usuario_id: int, tarefa_id: int):
    try:
        tarefa = alternar_status_api(usuario_id, tarefa_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))

    return {"dados": tarefa}
@router.delete("/usuarios/{usuario_id}/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_tarefa(usuario_id: int, tarefa_id: int):
    try:
        excluir_tarefa_api(usuario_id, tarefa_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro))